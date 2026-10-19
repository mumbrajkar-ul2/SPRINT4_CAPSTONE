# Historically grown decision logic used by both API and month-end reports.
import json
from pathlib import Path
def priority(status,severity,amount):
    if status=='CLOSED': return 'archive'
    if severity=='CRITICAL' or amount > 50000: return 'urgent'
    if severity=='HIGH' or status=='ESCALATED': return 'review'
    return 'queue'
def manual_review_required(status,severity):
    return severity in ('HIGH','CRITICAL') or status in ('ESCALATED','REOPENED')
HOLD_FOR_REVIEW='HOLD_FOR_REVIEW'
def evaluate_live_policy(region=None, year=None, question=None):
    """Live policy from contracts/decision-policies-archive.json.

    Returns HOLD_FOR_REVIEW when the archive is silent or no row matches.
    Does not return the JavaScript no-match default. Does not treat the Python urgent cutoff as a decided live limit.
    """
    if question=='urgent_amount_cutoff':
        return HOLD_FOR_REVIEW
    if region is None or year is None:
        return HOLD_FOR_REVIEW
    archive_path=Path(__file__).resolve().parents[1]/'contracts'/'decision-policies-archive.json'
    archive=json.loads(archive_path.read_text(encoding='utf-8'))
    year_s=str(year)
    for row in archive.get('historical_versions',[]):
        if row.get('region')==region and str(row.get('effective_from','')).startswith(year_s):
            return {'limit':row['limit'],'currency':row.get('currency','USD'),'region':region,'year':int(year_s),'rule':row.get('rule')}
    return HOLD_FOR_REVIEW
