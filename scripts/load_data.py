import asyncio 
import csv 
import sys 
from datetime import date, datetime 
from pathlib import Path 

from app.database import Base, Document, SessionLocal, engine 
from app.es_client import es, init_index 
from app.config import settings 

def parse_date(value: str) -> date: 
    value = value.strip() 
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y"):
        try:
            return datetime.strptime(value, fmt).date() 
        except ValueError:
            continue 
    raise ValueError(f'Не удалось распарсить: {value}') 

def parse_rubrics(value: str) -> list[str]:
    if not value: 
        return [] 
    return [r.strip() for r in value.split(",") if r.strip()] 

async def main(csv_path: Path) -> None: 
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all) 
    await init_index() 

    async with SessionLocal() as session: 
        with csv_path.open("r", encoding="utf-8") as f: 
            reader = csv.DictReader(f) 
            for row in reader:
                doc = Document(
                    text = row["text"], 
                    rubrics=parse_rubrics(row.get("rubrics", "")),
                    created_date=parse_date(row["created_at"]), 
                )
                session.add(doc) 
                await session.flush() 
                await es.index(
                    index=settings.index_name, 
                    id=str(doc.id), 
                    document={"id": doc.id, "text": doc.text},
                )
        await session.commit() 
    
    await es.indices.refresh(index=settings.index_name) 
    await es.close() 
    await engine.dispose() 
    print("OK") 

if __name__ == '__main__':
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "posts.csv") 
