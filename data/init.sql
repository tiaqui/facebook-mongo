\c scrapes;

CREATE TABLE IF NOT EXISTS posts(
    original_request_url VARCHAR(100),
    post_url VARCHAR(500),
    post_id  BIGINT PRIMARY KEY,
    texts VARCHAR(500),
    post_text VARCHAR(500),
    post_time TIMESTAMP,
    post_image VARCHAR(500),
    images VARCHAR(500),
    images_lowquality VARCHAR(500),
    images_description TEXT,
    images_lowquality_description TEXT,
    likes INT,
    comments INT,
    shares INT,
    link VARCHAR(500),
    user_ids BIGINT,
    username VARCHAR(500),
    user_url VARCHAR(500),
    reactions VARCHAR(50),
    reaction_count VARCHAR(50)
)
;

CREATE TABLE IF NOT EXISTS comments(
    comment_id BIGINT PRIMARY KEY,
    comment_url VARCHAR(100),
    commenter_id BIGINT NOT NULL,
    commenter_name VARCHAR(100),
    comment_text TEXT,
    comment_image VARCHAR(500),
    _post_id BIGINT NOT NULL
)
;

CREATE TABLE IF NOT EXISTS replies(
    comment_id BIGINT PRIMARY KEY,
    comment_url VARCHAR(100),
    commenter_id BIGINT NOT NULL,
    commenter_name VARCHAR(100),
    comment_text TEXT,
    comment_image VARCHAR(500),
    _comment_id BIGINT FOREIGN KEY
)
;