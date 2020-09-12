create table if not exists user (
  user_id integer primary key autoincrement,
  username string not null,
  email string not null,
  pw_hash string not null
);

create table if not exists message (
  message_id integer primary key autoincrement,
  author_id integer not null,
  add_stock_type string not null,
  register_stock_name_code string not null,
  register_stock_price string not null,
  register_stock_reason string not null,
  pub_date integer
);

create table if not exists follower (
  who_id integer,
  whom_id integer
);