CREATE TABLE IF NOT EXISTS news.articles (
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    keyword VARCHAR(50),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    originallink VARCHAR(200),
    link VARCHAR(200),
    pubdate TIMESTAMP,
    title VARCHAR(200),
    description MEDIUMTEXT
);
