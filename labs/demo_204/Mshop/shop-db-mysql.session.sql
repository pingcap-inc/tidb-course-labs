show databases;
INSERT INTO users (
    name,
    email,
    email_verified_at,
    password,
    type,
    remember_token,
    created_at,
    updated_at
  )
VALUES (
    'Tom',
    'Tom@lar.com',
     CURRENT_TIMESTAMP(3),
    '123456',
    'A',
    'Admin',
    CURRENT_TIMESTAMP(3),
    CURRENT_TIMESTAMP(3)
  );

INSERT INTO users (
    name,
    email,
    email_verified_at,
    password,
    type,
    remember_token,
    created_at,
    updated_at
  )
VALUES (
    'Jack',
    'Jack@lar.com',
     CURRENT_TIMESTAMP(3),
    '123456',
    'G',
    'User',
    CURRENT_TIMESTAMP(3),
    CURRENT_TIMESTAMP(3)
  );

  show create table users;

ALTER TABLE products CHANGE COLUMN price price DECIMAL(10, 2) NOT NULL;
