import asyncio

from utils.db_api.psql import Database


async def test():
    db = Database()
    await db.create()

    '''Get regions by lang'''
    regions_uz = await db.get_regions("uz")
    # print("Regions[uz]:", regions_uz)

    regions_ru = await db.get_regions("ru")
    # print("Regions[ru]:", regions_ru)

    '''Check user exists'''
    already_user = await db.user_exists(2222522)
    # print("User exists:", already_user)

    '''Get user by args'''
    user = await db.get_user()
    # print(user)

    '''Filter users'''
    users = await db.get_users_by(who_is="student")
    # print(users)

    '''Create user'''
    user_info = {
        "id": 123456,
        "lang": "uz",
        "full_name": "Alibek Valiyev",
        "phone_number": "998911234567",
        "who_is": "student",
        "region_id": 2
    }
    created = await db.create_user(user_info)
    # print(created)


if __name__ == "__main__":
    asyncio.run(test())
