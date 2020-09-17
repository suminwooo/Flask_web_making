create table if not exists user (
  user_id integer primary key autoincrement,
  username string not null,
  email string not null,
  pw_hash string not null
);

create table if not exists message (
  message_id integer primary key autoincrement,
  type integer not null,
  author_id integer not null,
  transaction_type string not null,
  code string not null,
  name string not null,
  price string not null,
  reason string not null,
  market string not null,
  pub_date integer
);

create table if not exists follower (
  who_id integer,
  whom_id integer
);
