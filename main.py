from fastapi import FastAPI, Request, Depends, HTTPException
from time import perf_counter

import db
import schemas

app = FastAPI(lifespan=db.lifespan, title='Моя API')
main_tag: list = ['Моя API']

async def get_pool():
    return app.state.pool

@app.middleware('http')
async def middleware_(request: Request, next_call):
    start_time = perf_counter()
    result = await next_call(request)
    duration = perf_counter() - start_time
    if duration > 0.1:
        print(f'Медленный запрос, заняло {duration:.4f}')
    return result

@app.get('/', tags=main_tag)
async def main_page():
    return schemas.ReturnForm(success=True, message='Healthy')

@app.get('/users', tags=main_tag)
async def get_users(pool = Depends(get_pool)):
    result = await db.get_users_db(pool)
    if result.success != True:
        if result.error_code == 'empty':
            raise HTTPException(status_code=404, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result

@app.post('/add_user', tags=main_tag)
async def add_user(user_data: schemas.UserDataForm, pool=Depends(get_pool)):
    result = await db.add_user_db(pool, user_data)
    if result.success != True:
        if result.error_code == 'conflict':
            raise HTTPException(status_code=409, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result

@app.delete('/clear', tags=main_tag)
async def clear_all(password: schemas.PasswordForm, pool = Depends(get_pool)):
    result = await db.clear_all_db(pool, password)
    if not result.success:
        if result.error_code == 'unauthorized':
            raise HTTPException(status_code=401, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result

@app.delete('/delete_user', tags=main_tag)
async def delete_user(user_id: schemas.UserIdForm, password: schemas.PasswordForm, pool = Depends(get_pool)):
    result = await db.delete_user_db(pool, user_id, password)
    if not result.success:
        if result.error_code == 'unauthorized':
            raise HTTPException(status_code=401, detail=result.message)
        if result.error_code == 'unknown_user':
            raise HTTPException(status_code=404, detail=result.message)
        raise HTTPException(status_code=500, detail=result.message)
    return result