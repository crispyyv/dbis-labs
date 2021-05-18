CREATE TABLE Region(
    region_id SERIAL PRIMARY KEY,
    Regname text,
    AreaName text,
    TerName  text,
    TerTypeName text,
    CONSTRAINT area_unique_constraint UNIQUE (Regname, AreaName, TerName)
);

