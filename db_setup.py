# coding: utf-8

import peewee
import model
import fetch_idol_data


def main():
    print('create table...')

    model.db.create_tables(
        [model.Tweet, model.Idol, model.Count, model.Update],
        True
    )

    print('success!')

    print('register cinderella girls...')

    data_source = fetch_idol_data.fetch()

    try:
        with model.db.transaction():
            model.Idol.insert_many(data_source).execute()

    except peewee.IntegrityError:
        model.db.rollback()

    print('success!')


if __name__ == '__main__':
    main()
