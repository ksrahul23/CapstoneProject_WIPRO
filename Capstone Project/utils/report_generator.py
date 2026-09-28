"""
Builds a self-contained HTML execution report from a list of step
results collected during the test run. No external report library is
required - this keeps the framework dependency-light and the report
portable (single file, screenshots referenced by relative path).
"""

import datetime
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config import config


class ReportGenerator:
    def __init__(self):
        self.steps = []
        self.start_time = datetime.datetime.now()

    def add_step(self, step_name: str, status: str, details: str = "", screenshot_path: str = None):
        self.steps.append({
            "step": step_name,
            "status": status,          # "PASS" | "FAIL"
            "details": details,
            "screenshot": os.path.relpath(screenshot_path, config.REPORTS_DIR) if screenshot_path else None,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        })

    def generate(self, output_path: str = None) -> str:
        output_path = output_path or os.path.join(config.REPORTS_DIR, "execution_report.html")
        end_time = datetime.datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        total = len(self.steps)
        passed = sum(1 for s in self.steps if s["status"] == "PASS")
        failed = total - passed
        overall = "PASS" if failed == 0 else "FAIL"

        rows = ""
        for s in self.steps:
            badge_class = "pass" if s["status"] == "PASS" else "fail"
            screenshot_html = (
                f'<a href="{s["screenshot"]}" target="_blank">'
                f'<img src="{s["screenshot"]}" class="thumb"/></a>'
                if s["screenshot"] else "N/A"
            )
            rows += f"""
            <tr>
                <td>{s['timestamp']}</td>
                <td>{s['step']}</td>
                <td><span class="badge {badge_class}">{s['status']}</span></td>
                <td>{s['details']}</td>
                <td>{screenshot_html}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>E-Commerce Automation - Execution Report</title>
<style>
  body {{ font-family: Arial, Helvetica, sans-serif; margin: 30px; color: #222; }}
  h1 {{ margin-bottom: 4px; }}
  .candidate-info {{ background: #f0f4f8; padding: 12px 18px; border-radius: 6px; margin: 15px 0; border-left: 4px solid #2c3e50; font-size: 14px; }}
  .candidate-info p {{ margin: 4px 0; }}
  .summary {{ display: flex; gap: 20px; margin: 20px 0 30px; }}
  .card {{ padding: 14px 22px; border-radius: 8px; color: #fff; min-width: 120px; text-align: center; }}
  .card.total {{ background: #445; }}
  .card.passed {{ background: #2e8b57; }}
  .card.failed {{ background: #c0392b; }}
  .card.duration {{ background: #555; }}
  .card .num {{ font-size: 26px; font-weight: bold; display: block; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 14px; vertical-align: middle; }}
  th {{ background: #2c3e50; color: #fff; }}
  tr:nth-child(even) {{ background: #f7f7f7; }}
  .badge {{ padding: 4px 10px; border-radius: 12px; color: #fff; font-size: 12px; font-weight: bold; }}
  .badge.pass {{ background: #2e8b57; }}
  .badge.fail {{ background: #c0392b; }}
  .thumb {{ width: 90px; border: 1px solid #ccc; border-radius: 4px; }}
  .overall {{ font-size: 18px; font-weight: bold; }}
</style>
</head>
<body>
  <h1>E-Commerce Web Automation - Execution Report</h1>
  <div class="candidate-info">
    <p><strong>Candidate Name:</strong> Rahul Kumar Shaw</p>
    <p><strong>Enrollment Number:</strong> 12023002022132</p>
    <p><strong>Department:</strong> CST</p>
  </div>
  <p>Application under test: {config.BASE_URL}</p>
  <p>Run started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} &nbsp;|&nbsp;
     Run ended: {end_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
  <p class="overall">Overall Result:
     <span class="badge {'pass' if overall=='PASS' else 'fail'}">{overall}</span>
  </p>

  <div class="summary">
    <div class="card total"><span class="num">{total}</span>Total Steps</div>
    <div class="card passed"><span class="num">{passed}</span>Passed</div>
    <div class="card failed"><span class="num">{failed}</span>Failed</div>
    <div class="card duration"><span class="num">{duration:.1f}s</span>Duration</div>
  </div>

  <table>
    <tr><th>Time</th><th>Step</th><th>Status</th><th>Details</th><th>Screenshot</th></tr>
    {rows}
  </table>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path
