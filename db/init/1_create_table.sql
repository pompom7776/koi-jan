-- DROP TABLE IF EXISTS send_reaction;
-- DROP TABLE IF EXISTS reaction;
-- DROP TABLE IF EXISTS send_chat;
-- DROP TABLE IF EXISTS vote;
-- DROP TABLE IF EXISTS select_tile;
-- DROP TABLE IF EXISTS riichi;
-- DROP TABLE IF EXISTS score_yaku;
-- DROP TABLE IF EXISTS yaku;
-- DROP TABLE IF EXISTS score;
-- DROP TABLE IF EXISTS agari;
-- DROP TABLE IF EXISTS call_tile;
-- DROP TABLE IF EXISTS call;
-- DROP TABLE IF EXISTS discard;
-- DROP TABLE IF EXISTS draw;
-- DROP TABLE IF EXISTS seat_wind;
-- DROP TABLE IF EXISTS round;
-- DROP TABLE IF EXISTS wall_tile;
-- DROP TABLE IF EXISTS tile;
-- DROP TABLE IF EXISTS wall;
-- DROP TABLE IF EXISTS game;
-- DROP TABLE IF EXISTS ready_room;
-- DROP TABLE IF EXISTS leave_room;
-- DROP TABLE IF EXISTS enter_room;
-- DROP TABLE IF EXISTS close_room;
-- DROP TABLE IF EXISTS create_room;
-- DROP TABLE IF EXISTS player_detail;
-- DROP TABLE IF EXISTS player;
-- DROP TABLE IF EXISTS room;

-- テーブル: room
CREATE TABLE room (
    id SERIAL PRIMARY KEY,
    room_number INT
);

-- テーブル: player
CREATE TABLE player (
    id SERIAL PRIMARY KEY
);

-- テーブル: player_detail
CREATE TABLE player_detail (
    id SERIAL PRIMARY KEY,
    player_id INT,
    name VARCHAR(8),
    socket_id TEXT,
    FOREIGN KEY (player_id) REFERENCES player(id)
);


-- テーブル: create_room
CREATE TABLE create_room (
    id SERIAL PRIMARY KEY,
    room_id INT,
    host_id INT,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id),
    FOREIGN KEY (host_id) REFERENCES player(id)
);

-- テーブル: close_room
CREATE TABLE close_room (
    id SERIAL PRIMARY KEY,
    room_id INT,
    close_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id)
);

-- テーブル: enter_room
CREATE TABLE enter_room (
    id SERIAL PRIMARY KEY,
    room_id INT,
    player_id INT,
    enter_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id),
    FOREIGN KEY (player_id) REFERENCES player(id)
);

-- テーブル: leave_room
CREATE TABLE leave_room (
    id SERIAL PRIMARY KEY,
    room_id INT,
    player_id INT,
    leave_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id),
    FOREIGN KEY (player_id) REFERENCES player(id)
);

-- テーブル: ready_room
CREATE TABLE ready_room (
    id SERIAL PRIMARY KEY,
    room_id INT,
    player_id INT,
    ready_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id),
    FOREIGN KEY (player_id) REFERENCES player(id)
);

-- テーブル: game
CREATE TABLE game (
    id SERIAL PRIMARY KEY,
    room_id INT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id)
);

-- テーブル: wall
CREATE TABLE wall (
    id SERIAL PRIMARY KEY,
    remaining_number INT,
    dora_number INT
);

-- テーブル: tile
CREATE TABLE tile (
    id SERIAL PRIMARY KEY,
    suit VARCHAR(6),
    rank INT,
    name VARCHAR(5)
);

-- テーブル: wall_tile
CREATE TABLE wall_tile (
    id SERIAL PRIMARY KEY,
    wall_id INT,
    tile_id INT,
    FOREIGN KEY (wall_id) REFERENCES wall(id),
    FOREIGN KEY (tile_id) REFERENCES tile(id)
);

-- テーブル: round
CREATE TABLE round (
    id SERIAL PRIMARY KEY,
    game_id INT,
    round_number INT,
    round_wind VARCHAR(5),
    dealer_id INT,
    wall_id INT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES game(id),
    FOREIGN KEY (dealer_id) REFERENCES player(id),
    FOREIGN KEY (wall_id) REFERENCES wall(id)
);

-- テーブル: seat_wind
CREATE TABLE seat_wind (
    id SERIAL PRIMARY KEY,
    round_id INT,
    player_id INT,
    wind VARCHAR(5),
    FOREIGN KEY (round_id) REFERENCES round(id),
    FOREIGN KEY (player_id) REFERENCES player(id)
);

-- テーブル: draw
CREATE TABLE draw (
    id SERIAL PRIMARY KEY,
    round_id INT,
    player_id INT,
    tile_id INT,
    draw_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (round_id) REFERENCES round(id),
    FOREIGN KEY (player_id) REFERENCES player(id),
    FOREIGN KEY (tile_id) REFERENCES tile(id)
);

-- テーブル: discard
CREATE TABLE discard (
    id SERIAL PRIMARY KEY,
    round_id INT,
    player_id INT,
    tile_id INT,
    discard_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (round_id) REFERENCES round(id),
    FOREIGN KEY (player_id) REFERENCES player(id),
    FOREIGN KEY (tile_id) REFERENCES tile(id)
);

-- テーブル: call
CREATE TABLE call (
    id SERIAL PRIMARY KEY,
    round_id INT,
    type VARCHAR(9),
    call_player_id INT,
    target_player_id INT,
    target_tile_id INT,
    call_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (round_id) REFERENCES round(id),
    FOREIGN KEY (call_player_id) REFERENCES player(id),
    FOREIGN KEY (target_player_id) REFERENCES player(id),
    FOREIGN KEY (target_tile_id) REFERENCES tile(id)
);

-- テーブル: call_tile
CREATE TABLE call_tile (
    id SERIAL PRIMARY KEY,
    call_id INT,
    tile_id INT,
    FOREIGN KEY (call_id) REFERENCES call(id),
    FOREIGN KEY (tile_id) REFERENCES tile(id)
);

-- テーブル: agari
CREATE TABLE agari (
    id SERIAL PRIMARY KEY,
    round_id INT,
    player_id INT,
    target_player_id INT,
    target_tile_id INT,
    type VARCHAR(5),
    agari_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (round_id) REFERENCES round(id),
    FOREIGN KEY (player_id) REFERENCES player(id),
    FOREIGN KEY (target_player_id) REFERENCES player(id),
    FOREIGN KEY (target_tile_id) REFERENCES tile(id)
);

-- テーブル: score
CREATE TABLE score (
    id SERIAL PRIMARY KEY,
    agari_id INT,
    score INT,
    han INT,
    fu INT,
    FOREIGN KEY (agari_id) REFERENCES agari(id)
);

-- テーブル: yaku
CREATE TABLE yaku (
    id SERIAL PRIMARY KEY,
    en_name TEXT,
    ja_name TEXT
);

-- テーブル: score_yaku
CREATE TABLE score_yaku (
    id SERIAL PRIMARY KEY,
    score_id INT,
    yaku_id INT,
    FOREIGN KEY (score_id) REFERENCES score(id),
    FOREIGN KEY (yaku_id) REFERENCES yaku(id)
);

-- テーブル: riichi
CREATE TABLE riichi (
    id SERIAL PRIMARY KEY,
    round_id INT,
    player_id INT,
    tile_id INT,
    riichi_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (round_id) REFERENCES round(id),
    FOREIGN KEY (player_id) REFERENCES player(id),
    FOREIGN KEY (tile_id) REFERENCES tile(id)
);

-- テーブル: select
CREATE TABLE select_tile (
    id SERIAL PRIMARY KEY,
    round_id INT,
    player_id INT,
    tile_id INT,
    select_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (round_id) REFERENCES round(id),
    FOREIGN KEY (player_id) REFERENCES player(id),
    FOREIGN KEY (tile_id) REFERENCES tile(id)
);

-- テーブル: vote
CREATE TABLE vote (
    id SERIAL PRIMARY KEY,
    round_id INT,
    vote_player_id INT,
    target_player_id INT,
    vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (round_id) REFERENCES round(id),
    FOREIGN KEY (vote_player_id) REFERENCES player(id),
    FOREIGN KEY (target_player_id) REFERENCES player(id)
);

-- テーブル: send_chat
CREATE TABLE send_chat (
    id SERIAL PRIMARY KEY,
    room_id INT,
    player_id INT,
    message TEXT,
    send_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id),
    FOREIGN KEY (player_id) REFERENCES player(id)
);

-- テーブル: reaction
CREATE TABLE reaction (
    id SERIAL PRIMARY KEY,
    name TEXT
);

-- テーブル: send_reaction
CREATE TABLE send_reaction (
    id SERIAL PRIMARY KEY,
    room_id INT,
    player_id INT,
    reaction_id INT,
    send_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES room(id),
    FOREIGN KEY (player_id) REFERENCES player(id),
    FOREIGN KEY (reaction_id) REFERENCES reaction(id)
);
