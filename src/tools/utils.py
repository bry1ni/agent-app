import json
from typing import Any

from email.message import EmailMessage
import smtplib, os, html
from typing import List, Tuple
import json, re

from src.config.prompts import EMAIL_SUBJECT, EMAIL_HTML, EMAIL_TEXT


def format_tool_output(tool_message: Any) -> str:
	"""
	Formats the tool message into a JSON string ensuring it's always a valid str.

	Args:
	    tool_message (Any): The tool message to be converted (typically a dict).

	Returns:
	    str: JSON formatted string representation of the tool message.
	"""
	return json.dumps(tool_message, ensure_ascii=False)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "d.fettache@esi-sba.dz"
SMTP_PASS = "mkptddorddyopdyc"


def _html_rows(table: List[Tuple[str, str]]) -> str:
	return "\n".join(
		f"<tr><td style='padding:10px 12px;border-top:1px solid #e9ecf8;'>{html.escape(i)}</td>"
		f"<td style='padding:10px 12px;border-top:1px solid #e9ecf8;'>{html.escape(a)}</td></tr>"
		for i, a in table
	)

def _html_list(recs: List[str]) -> str:
	return "\n".join(f"<li>{html.escape(r)}</li>" for r in recs)


def render_email(first_name: str,
				insight_table: List[Tuple[str, str]],
				recs: List[str],
				dashboard_url: str,
				tasks_line: str = "",
				your_name: str = "Ayor AI Consultant"):

	ctx = dict(
		subject=EMAIL_SUBJECT,
		first_name=first_name,
		insight_rows=_html_rows(insight_table),
		recommendation_items=_html_list(recs),
		dashboard_url=dashboard_url,
		your_name=your_name,
		plain_insight="; ".join(f"{i} → {a}" for i, a in insight_table),
		plain_recommendations="\n".join(f"- {r}" for r in recs),
		tasks_line_html=(
			f"<pre style='font-family:monospace;font-size:13px;margin-top:24px'>{tasks_line}</pre>"
			if tasks_line else ""
		),
		tasks_line_text=f"\n\n{tasks_line}" if tasks_line else "",
	)

	html_body = EMAIL_HTML.format(**ctx) + ctx["tasks_line_html"]
	text_body = EMAIL_TEXT.format(**ctx) + ctx["tasks_line_text"]
	return html_body, text_body

def send(to: str,
		first_name: str,
		insight_table: List[Tuple[str, str]],
		recs: List[str],
		dashboard_url: str,
		tasks_line: str = ""):
	html_body, text_body = render_email(first_name, insight_table, recs, dashboard_url)
	msg = EmailMessage()
	msg["Subject"] = EMAIL_SUBJECT
	msg["From"] = SMTP_USER
	msg["To"] = to
	msg.set_content(text_body)
	msg.add_alternative(html_body, subtype="html")

	with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
		s.starttls()
		s.login(SMTP_USER, SMTP_PASS)
		s.send_message(msg)
 
 
TASK_RE = re.compile(r'^TASK:\s*(\{.*\})\s*$', re.I)

def split_recs_and_tasks(recs: List[str]) -> Tuple[List[str], str]:
	"""
	• Strip lines that start with 'TASK:' from `recs`
	• Return (clean_recommendations, tasks_json_line)

	tasks_json_line  →  ''  or  'TASKS:[{...},{...}]'
	"""
	tasks, clean = [], []
	for line in recs:
		m = TASK_RE.match(line.strip())
		if m:
			try:
				tasks.append(json.loads(m.group(1)))
			except json.JSONDecodeError:
				clean.append(line)  # leave bad task in text form
		else:
			clean.append(line)

	tasks_line = f"TASKS={json.dumps(tasks, separators=(',', ':'))}" if tasks else ""
	return clean, tasks_line
