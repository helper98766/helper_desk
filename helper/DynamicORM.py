import os
import sys
import logging
from sqlalchemy import Column, Integer, String, Boolean, VARCHAR, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class ORMClassGenerator:
    def __init__(self, engine):
        self.engine = engine
        self.metadata = MetaData(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_dynamic_class(self, columns, primary_key):
        dynamic_column = []
        for col_name, col_type in columns.items():
            dynamic_column.append(
                f"  {col_name}=Column({col_type.capitalize()}, primary_key={'True' if col_name == primary_key else 'False'})"
            )
        return dynamic_column

    def mapping_file(self, table_name, column):
        class_code = f"""
    from sqlalchemy import Column, Integer, String, Boolean, VARCHAR, MetaData
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

        class {table_name}(Base):
            __tablename__ = '{table_name}'
        {chr(10).join(column)}
        """
        return class_code

    def create_orm_class(self, class_code, table_name):
        namespace = {}
        exec(class_code, namespace)
        return namespace[table_name]

    def fetch_all_data(self, orm_class):
        session = self.Session()
        try:
            result = session.query(orm_class).all()
            logging.info(f"Length of records: {len(result)}")
            if result:
                for row in result:
                    if row is not None:
                        self.creating_dict_of_fetched_data(row)
                    else:
                        logging.info("Empty data")
        except Exception as e:
            logging.error(f"Error fetching the data: {e}")
        finally:
            session.close()

    def fetch_data_with_filter(self, orm_class, filter_condition):
        session = self.Session()
        try:
            result = session.query(orm_class).filter(filter_condition).all()
            logging.info(f"Length of records: {len(result)}")
            if result:
                for row in result:
                    if row is not None:
                        self.creating_dict_of_fetched_data(row)
                    else:
                        logging.info("Empty data")
        except Exception as e:
            logging.error(f"Error fetching filtered data: {e}")
        finally:
            session.close()

    def creating_dict_of_fetched_data(self, row):
        column_value = {key: ("NULL" if value is None else value) for key, value in row.__dict__.items() if not key.startswith('_')}
        logging.info(column_value)

    def insert_data(self, orm_class, data, table_name, primary_key):
        session = self.Session()
        try:
            primary_key_value = data[f"{primary_key}"]
            condition = getattr(orm_class, primary_key)
            existing_record = session.query(orm_class).filter(condition == primary_key_value).first()

            if existing_record:
                logging.info(f"Data already exists with primary key : {primary_key_value}. Enter unique Primary Key")
            else:
                obj = orm_class(**data)
                session.add(obj)
                session.commit()
                logging.info(f"Data has been saved to {table_name}")
        except Exception as e:
            session.rollback()
            logging.error(f"Error Inserting data: {e}")
        finally:
            session.close()

    def update_data(self, orm_class, primary_key_value, data):
        session = self.Session()
        try:
            obj = session.query(orm_class).get(primary_key_value)
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                session.commit()
                logging.info("Updated row successfully")
            else:
                logging.info(f"Invalid value of primary_key :{primary_key_value}. Enter Valid Primary Key")
        except Exception as e:
            session.rollback()
            logging.error(f"Error Updating data: {e}")
        finally:
            session.close()

    def delete_all(self, orm_class):
        session = self.Session()
        try:
            session.query(orm_class).delete()
            session.commit()
            logging.info("Deleted successfully")
        except Exception as e:
            session.rollback()
            logging.error(f"Error Deleting data: {e}")
        finally:
            session.close()

    def delete_filtered_data(self, orm_class, **filters):
        session = self.Session()
        try:
            query = session.query(orm_class)
            for col_name, value in filters.items():
                query = query.filter(getattr(orm_class, col_name) == value)
            query.delete()
            session.commit()
            logging.info("Deleted filtered data")
        except Exception as e:
            session.rollback()
            logging.error(f"Error Deleting data: {e}")
        finally:
            session.close()

    def save_class_to_file(self, class_code, file_name):
        if os.path.exists(file_name):
            logging.info(f"File already exists with name {file_name}")
        else:
            with open(file_name, "w") as file:
                file.write(class_code)
                logging.info(f"ORM Class has been saved to {file_name}.")

    def get_session(self):
        return self.Session()
