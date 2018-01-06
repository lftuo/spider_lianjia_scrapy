create table spider_lianjia.spider_lianjia_new_house(
  city_name VARCHAR(100) character set utf8 NOT NULL default '',
  area_name VARCHAR(100) character set utf8 NOT NULL default '',
  house_name VARCHAR(200) character set utf8 NOT NULL default '',
  house_where VARCHAR(500) character set utf8 NOT NULL default '',
  house_area VARCHAR(200) character set utf8 NOT NULL default '',
  house_price VARCHAR(200) character set utf8 NOT NULL default '',
  house_url VARCHAR(200) NOT NULL DEFAULT ''
) DEFAULT CHARSET = utf8;