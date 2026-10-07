from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession 

from app.config import settings 
from app.database import Document, get_session 
from app.es_client import es 
from app.schemas import DocumentOut 

router = APIRouter(tags=["documents"]) 

ES_CANDIDATES_LIMIT = 1000

@router.get("/search", response_model=list[DocumentOut], summary="Поиск документов по тексту")
async def search_documents(
    q: str = Query(..., min_length=1, description="Произвольный текстовый запрос"), 
    session: AsyncSession = Depends(get_session),
) -> list[Document]:
    resp = await es.search(
        index = settings.index_name, 
        query = {"match": {"text": q}}, 
        size = ES_CANDIDATES_LIMIT, 
        _source = ["id"], 
    )
    ids = [int(hit["_source"]["id"]) for hit in resp["hits"]["hits"]] 
    if not ids: 
        return [] 
    
    result = await session.execute(
        select(Document).where(Document.id.in_(ids)).order_by(Document.created_date.desc())
        .limit(20) 
    )
    return list(result.scalars().all()) 

@router.delete("/documents/{doc_id}", status_code=204, summary="Удалить документ по id") 
async def delete_document(doc_id: int, session: AsyncSession = Depends(get_session)) -> None:
    doc = await session.get(Document, doc_id) 
    if doc is None: 
        raise HTTPException(status_code=404, detail="Document not found!") 
    
    await session.delete(doc) 
    await session.commit() 

    try:
        await es.delete(index=settings.index_name, id=str(doc_id), refresh=True) 
    except Exception: 
        pass 
    