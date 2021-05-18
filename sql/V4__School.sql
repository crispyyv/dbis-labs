CREATE TABLE School(school_id SERIAL PRIMARY KEY NOT NULL UNIQUE,
                                                          EOName text, EOTypeName text, EOParent text, region_id int, CONSTRAINT school_unique_constraint UNIQUE (EOName), CONSTRAINT school_territory
                    FOREIGN KEY(region_id) REFERENCES Region (region_id));


