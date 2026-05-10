#!/bin/bash
# Daily report script - called by cron at 8:00 AM
# Sends blog progress report to Yanick via telegram

cd /root/.openclaw/workspace/aitools-blog
python3 daily_report.py > /tmp/daily_report_output.txt 2>&1

# The report will be picked up by the agent during heartbeat
# and delivered to Yanick
touch /root/.openclaw/workspace/aitools-blog/.report_ready
