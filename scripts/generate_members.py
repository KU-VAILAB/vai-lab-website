import pandas as pd
from datetime import date
import os
import re
import hashlib

def slugify(text):
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-]', '', text)
    return text

def create_member_posts():
    csv_path = '/Users/woosung/Desktop/KU/LabIntern/vai-lab-website/_data/members.csv'
    output_dir = '/Users/woosung/Desktop/KU/LabIntern/vai-lab-website/_pages/team/_posts'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_csv(csv_path)

    # Mapping columns based on the CSV header
    # 0: 타임스탬프
    # 1: 연구실 용 이메일 -> email
    # 2: 이름 -> name, title
    # 3: Research Interest -> interest
    # 4: 사진
    # 5: 이메일 주소
    # 6: 학위 과정 -> role
    # 7: 현재 소속
    # 8: 개인 웹사이트 -> social.website
    # 9: 사진 공개 링크 -> image

    for _, row in df.iterrows():
        name = str(row['이름']).strip().title()
        email = str(row['연구실 용 이메일']).strip()
        interest = str(row['Research Interest (최대한 선택지 안에서 골라달라고 하셨습니다)']).strip()
        role = str(row['학위 과정']).strip()
        website = str(row['개인 웹사이트']).strip()
        image = str(row['사진 공개 링크']).strip()
        affiliation = str(row['현재 소속 (파트타임 분들만 부탁드립니다)']).strip()

        category = "intern" if role == "intern" else "student"

        # Handle nan/empty values
        if website == 'nan' or not website:
            website = ''
        if interest == 'nan' or not interest:
            interest = ''
        if affiliation == 'nan' or not affiliation:
            affiliation = 'Korea University'
        else:
            affiliation = f'Korea University & {affiliation}'

        # Format interest as a single list item (matching template)
        interest_str = f' - {interest}' if interest else ''

        content = f"""---
layout: member
category: {category}
name: {name}
title: {name}
email: {email}
image: {image}
role: {role}
affiliation: {affiliation}
social:
    website: {website}
interest:
{interest_str}
---
"""

        # Filename: YYYY-MM-DD-researcher-name.md
        # Using today's date

        filename_date = date.today().isoformat()
        # Generate a short hash from email to avoid collisions
        email_hash = hashlib.md5(email.encode()).hexdigest()[:4]
        filename = f"{filename_date}-researcher-{slugify(name)}-{email_hash}.md"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {file_path}")

if __name__ == "__main__":
    create_member_posts()
