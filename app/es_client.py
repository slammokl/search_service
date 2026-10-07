from elasticsearch import AsyncElasticsearch 
from app.config import settings 

es = AsyncElasticsearch(settings.elasticsearch_url) 

async def init_index() -> None: 
    exists = await es.indices.exists(index=settings.index_name) 
    if not exists: 
        await es.indices.create(
            index = settings.index_name,
            mappings={
                "properties": {
                    "id": {"type": "integer"},
                    "text": {"type": "text"}, 
                }
            },
        )