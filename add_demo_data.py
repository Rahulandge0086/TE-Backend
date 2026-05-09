import asyncio
import uuid
from src.database.prisma_client import get_prisma
from src.database.supabase_save import SupabaseSaver

async def main():
    p = get_prisma()
    
    # 1. Create a demo organization
    org_id = str(uuid.uuid4())
    org = p.organization.create(data={
        'id': org_id,
        'name': 'Demo Corp',
        'slug': f'demo-corp-{str(uuid.uuid4())[:8]}',
    })
    
    # 2. Create a demo user (master user)
    user_id = str(uuid.uuid4())
    user = p.user.create(data={
        'id': user_id,
        'orgId': org_id,
        'email': f'admin-{str(uuid.uuid4())[:8]}@democorp.com',
        'fullName': 'Demo Admin',
        'isMasterUser': True
    })
    
    # Update org with master user
    p.organization.update(
        where={'id': org_id},
        data={'masterUserId': user_id}
    )
    
    # 3. Create demo Ishikawa and 5 Whys data
    ishikawa_data = [{
        'id': 1,
        'category': 'Machine',
        'result': [{
            'sub_category': 'Calibration',
            'cause': 'Torque wrench was out of calibration',
            'evidence': 'Maintenance log shows skipped cycle',
            'severity': 'High',
            'status': 'confirmed'
        }]
    }]
    
    five_whys_data = [{
        'problem_id': 'cause-1',
        'root_cause': 'Lack of automated maintenance alerts in legacy system',
        'confidence': 0.95,
        'why_chain': [
            {'level': 1, 'question': 'Why?', 'answer': 'Torque failed'},
            {'level': 2, 'question': 'Why?', 'answer': 'Wrench not calibrated'}
        ]
    }]
    
    # 4. Save analysis using our SupabaseSaver class
    saver = SupabaseSaver()
    result = saver.save_analysis(
        user_id=user_id,
        master_user_id=user_id,
        org_id=org_id,
        query='Connector torque failure during assembly',
        domain='Manufacturing',
        past_record=5,
        session_title='Demo Investigation',
        ishikawa=ishikawa_data,
        five_whys=five_whys_data
    )
    
    print(f'\n--- Demo Data Created Successfully ---')
    print(f'Organization ID: {org_id}')
    print(f'User ID: {user_id}')
    print(f'Session ID: {result.get("session_id")}')
    print(f'Ishikawa ID: {result.get("ishikawa_id")}')
    print(f'5-Whys ID: {result.get("five_whys_id")}')
    
if __name__ == '__main__':
    asyncio.run(main())
