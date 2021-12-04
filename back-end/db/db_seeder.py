from sqlalchemy import create_engine
from os import environ

connection_string = environ["DB_URL"]
engine = create_engine(connection_string)

engine.execute("""
    INSERT INTO users (username, card, first_name, last_name, is_staff, hashed_password, disabled) VALUES ('stlpik', '1234567891011', 'Meno', 'Priezvisko', true, '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', false), ('stud', '1234567891012', 'Meno', 'Priezvisko', false, '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', false);
    INSERT INTO groups (name) VALUES ('LinuxPP');
    INSERT INTO time_spec (title, weekday_mask, time_from, time_to, date_to) VALUES ('pracovne dni vecer', 31, '17:00:00', '22:00:00', '2022-01-01 00:00:00'), ('pondelok rano', 1, '07:00:00', '10:00:00', '2022-06-01 00:00:00');
    INSERT INTO access_point_type (name) VALUES ('H3'), ('H6'), ('T1');
    INSERT INTO rules (name, allow, time_spec_id, ap_type_id) VALUES ('H6_LinuxPP', true, 1, 1);
    INSERT INTO user_group (user_id, group_id) VALUES (1, 1);
    INSERT INTO group_rule (group_id, rule_id) VALUES (1, 1);
    INSERT INTO access_point (name, type_id) VALUES ('H6 zadne dvere', 2), ('H6 bocne dvere', 2);
""")
