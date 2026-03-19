import asyncio
import logging

# Standard logging config for production-ready observability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_optimized_tasks(tasks):
    """
    Core execution engine for concurrent I/O workloads.
    
    Setting return_exceptions=True is a deliberate design choice 
    to prevent the 'cascading failure' pattern typical in SaaS pipelines.
    """
    try:
        # We allow individual tasks to fail without crashing the whole loop
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Post-execution cleanup: Filter out exceptions and log failures
        clean_results = []
        for res in results:
            if isinstance(res, Exception):
                logger.error(f"Async worker encountered an error: {res}")
            else:
                clean_results.append(res)
                
        return clean_results
    
    except Exception as e:
        # Global catch-all for high-level pipeline orchestration issues
        logger.critical(f"Pipeline orchestration failed: {str(e)}")
        return []
