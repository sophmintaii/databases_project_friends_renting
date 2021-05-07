CREATE TABLE IF NOT EXISTS "user_" (
	"id" serial,
	"phone_number" varchar(12) unique,
	"name" varchar(40) not null,
	"surname" varchar(40),
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "friend" (
	"id" serial,
	"phone_number" varchar(12) unique,
	"name" varchar(40) not null,
	"surname" varchar(40),
	"description" varchar(300) not null,
	"age" int not null,
	"gender" boolean,
	PRIMARY KEY ("id")
);


CREATE TABLE IF NOT EXISTS "party" (
	"party_id" serial,
	"name" varchar not null,
	PRIMARY KEY ("party_id")
);

CREATE TABLE IF NOT EXISTS "rent" (
	"rent_id" serial,
	"user_id" int not null,
	"date" date not null,
	"party_id" int,
	PRIMARY KEY ("rent_id"),
	CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
	  REFERENCES user_(id)

);

CREATE TABLE IF NOT EXISTS "rent_friends" (
	"rent_id" int not null,
	"friend_id" int not null,
	CONSTRAINT fk_friend
      FOREIGN KEY(friend_id) 
	  REFERENCES friend(id),
	CONSTRAINT fk_rent
      FOREIGN KEY(rent_id) 
	  REFERENCES rent(rent_id)
);


CREATE TABLE IF NOT EXISTS "dayoffs" (
	"friend_id" int not null,
	"date" date not null,
	CONSTRAINT fk_friend
      FOREIGN KEY(friend_id) 
	  REFERENCES friend(id)
);


CREATE TABLE IF NOT EXISTS "complaint" (
	"complaint_id" serial,
	"text" varchar(200) not null,
	"friend_id" int not null,
	"date" date not null,
	PRIMARY KEY ("complaint_id"),
	CONSTRAINT fk_friend
      FOREIGN KEY(friend_id) 
	  REFERENCES friend(id)
);


CREATE TABLE IF NOT EXISTS "user_complaint" (
	"user_id" int not null,
	"complaint_id" int not null,
	CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
	  REFERENCES user_(id),
	CONSTRAINT fk_complaint
      FOREIGN KEY(complaint_id) 
	  REFERENCES complaint(complaint_id)
);


CREATE TABLE IF NOT EXISTS "present" (
	"present_id" serial,
	"name" varchar(100),
	"price" decimal(20, 5),
	PRIMARY KEY ("present_id")
);

CREATE TABLE IF NOT EXISTS "present_given" (
	"given_id" serial,
	"present_id" int not null,
	"user_id" int not null,
	"friend_id" int not null,
	"date" date not null,
	"is_returned" boolean not null,
	PRIMARY KEY ("given_id"),
	CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
	  REFERENCES user_(id),
	CONSTRAINT fk_friend
      FOREIGN KEY(friend_id) 
	  REFERENCES friend(id),
	CONSTRAINT fk_present
      FOREIGN KEY(present_id) 
	  REFERENCES present(present_id)
);


CREATE TABLE IF NOT EXISTS "hobby" (
	"hobby_id" serial,
	"name" varchar(30) unique,
	PRIMARY KEY ("hobby_id")
);



CREATE TABLE IF NOT EXISTS "friend_hobby" (
	"friend_id" int not null,
	"hobby_id" int not null,
	CONSTRAINT fk_friend
      FOREIGN KEY(friend_id) 
	  REFERENCES friend(id),
	CONSTRAINT fk_hobby
      FOREIGN KEY(hobby_id) 
	  REFERENCES hobby(hobby_id)
);

----------------------------------------------- З А П О В Н Е Н Н Я -------------------------------------

-- insert users
insert into user_ (id, phone_number, name, surname) values (1, '553-453-4048', 'Fredrick', 'McGerraghty');
insert into user_ (id, phone_number, name, surname) values (2, '185-785-8016', 'Devan', 'Hobble');
insert into user_ (id, phone_number, name, surname) values (3, '665-883-2126', 'Fraze', 'Tearney');
insert into user_ (id, phone_number, name, surname) values (4, '627-694-3054', 'Frasco', 'Packe');
insert into user_ (id, phone_number, name, surname) values (5, '261-613-7599', 'Elwira', 'Werner');
insert into user_ (id, phone_number, name, surname) values (6, '603-148-4277', 'Aida', 'Asipenko');
insert into user_ (id, phone_number, name, surname) values (7, '275-415-6638', 'Bent', 'Gamblin');
insert into user_ (id, phone_number, name, surname) values (8, '619-426-8073', 'Virgina', 'Balf');
insert into user_ (id, phone_number, name, surname) values (9, '241-597-2905', 'Mariette', 'Durrett');
insert into user_ (id, phone_number, name, surname) values (10, '880-905-7560', 'Garvey', 'Penquet');

--insert friends
insert into friend (id, phone_number, name, surname, description, age, gender) values 
(1, '686-544-9461', 'Ingelbert', 'Faircliffe', 'Funny and easy-going. Love football', 20, '0'),
(2, '264-147-3967', 'Rachel', 'MacAdie', 'Know everything about Italy.', 25, '1'),
(3, '787-148-7783', 'Chrysa', 'Winspare', 'Smart and funny. We will have fun together!', 21, '1'),
(4, '923-713-1208', 'Fletcher', 'Hillum', 'Professional drinking companion!', 19, '0'),
(5, '429-340-4046', 'Joe', 'Crosetti', 'Positive and charming. Call me if you are bored and we will have fun!', 22, '0'),
(6, '868-310-1250', 'Sonny', 'Prigmore', 'Like reading and playing guitar. We can jam together, call!', 30, '1'),
(7, '886-431-8750', 'Averil', 'Weber', 'I am the best friend you can find here, do not loose your chance!', 34, '1'),
(8, '815-997-0575', 'Kean', 'Spaughton', 'Can talk about everything, but can also be quiet.', 20, '0'),
(9, '329-772-0523', 'Ced', 'Reoch', 'Let`s drink cider and talk about everything!', 22, '1'),
(10, '243-194-8408', 'Joela', 'Feeley', 'The best drinking companion you can have!', 24, '0');

--insert parties
insert into party (party_id, name) values
(1, 'New Year'),
(2, 'Christmas'),
(3, 'Birthday party'),
(4, 'St. Valentine'),
(5, 'Thanksgiving Day'),
(6, 'Bachelor party for boys'),
(7, 'Bachelor party for girls'),
(8, 'Marriage'),
(9, 'Independence Day'),
(10, 'Your custom party');

--insert rent
INSERT INTO rent (rent_id, user_id, party_id, date) VALUES 
(1, 2, null, '2020-09-13'),
(2, 6, 3, '2020-09-18'),
(3, 1, null, '2020-10-05'),
(4, 10, 6, '2020-11-11'),
(5, 4, 1, '2020-12-31'),
(6, 3, null, '2021-01-09'),
(7, 5, null, '2021-01-28'),
(8, 9, 4, '2021-02-14'),
(9, 7, null, '2021-03-28'),
(10, 8, null, '2021-04-02'),
(11, 6, 3, '2021-04-13');

--insert friends in corresponding rents
INSERT INTO rent_friends(rent_id, friend_id) VALUES
(1, 2),
(1, 3),
(2, 5),
(2, 8),
(2, 10),
(3, 1),
(3, 2),
(3, 5),
(4, 5),
(5, 9),
(5, 7),
(6, 1),
(7, 4),
(7, 3),
(8, 10),
(9, 6),
(9, 9),
(9, 10),
(10, 3),
(10, 5),
(11, 5),
(11, 8);

INSERT INTO dayoffs(friend_id, date) VALUES
(1, '2020-11-07'),
(1, '2020-11-08'),
(2, '2020-11-12'),
(2, '2020-11-13'),
(3, '2021-01-06'),
(3, '2020-01-07'),
(4, '2021-01-06'),
(4, '2020-01-07'),
(6, '2020-01-20'),
(7, '2020-02-15'),
(5, '2020-02-29'),
(1, '2020-03-01'),
(10, '2020-04-07');

INSERT INTO hobby(hobby_id, name) VALUES 
(1, 'Music'),
(2, 'Guitar'),
(3, 'Art'),
(4, 'Sport'),
(5, 'Football'),
(6, 'Knitting'),
(7, 'Hockey'),
(8, 'Photography'),
(9, 'Travelling'),
(10, 'Skateboarding'),
(11, 'Gaming');

INSERT INTO friend_hobby (friend_id, hobby_id) VALUES 
(1, 1),
(1, 2),
(1, 8),
(2, 1),
(2, 11),
(3, 2),
(3, 6),
(4, 3),
(4, 10),
(5, 11),
(5, 10),
(6, 4),
(7, 1),
(7, 9),
(8, 4),
(8, 6),
(9, 7),
(10, 8);

--insert present
INSERT INTO present (present_id, name, price) VALUES
(1, 'phone', 39999),
(2, 'flowers, necklace', 17000),
(3, 'Backpack, book, decorated cake', 1056.5),
(4, 'A set of accessories for hiking', 2004.1),
(5, 'Certificate for skydiving', 5999),
(6, 'Gift card for shopping', 2000),
(7, 'Weekend ticket to Italy', 2674),
(8, 'Louis Vuitton bag', 40000),
(9, 'Champagne and a day trip to the amusement park', 3205.8),
(10, 'Perfumes', 4999.5);

--insert given presents
INSERT INTO present_given(given_id, present_id, user_id, friend_id, date, is_returned) VALUES
(1, 4, 6, 5, '2020-09-18', true),
(2, 8, 6, 8, '2020-09-18', true),
(3, 10, 6, 10, '2020-09-18', true),
(4, 7, 10, 5, '2020-11-11', true),
(5, 2, 4, 9, '2020-12-31',true),
(6, 6, 4, 7, '2020-12-31', false),
(7, 1, 9, 10, '2021-02-14', true),
(8, 3, 6, 5, '2021-04-13', true),
(9, 9, 6, 8, '2021-04-13', true);

--insert complaint
INSERT INTO complaint(complaint_id, text, friend_id, date) VALUES
(1,'A hired friend was 1 hour late', 9, '2021-01-01'),
(2, 'Hired friend still has not returned the present', 7, '2021-01-10'),
(3, 'Terrible outfit of my fake boyfriend', 10, '2021-02-15'),
(4, 'The friend was very silent and uninteresting', 5, '2020-09-18'),
(5, 'The friend does not respond to messages and calls for a long time' , 2, '2020-09-15'),
(6, 'Stole my wallet', 1, '2020-10-06');

--insert user complaint
INSERT INTO user_complaint(user_id, complaint_id) VALUES
(4, 1),
(4, 2),
(9, 3),
(6, 4),
(2, 5),
(1, 6);



---------------------------------------------- З А П И Т И ----------------------------------------

-- 1. Для клієнта С знайти усіх друзів, яких він наймав принаймні N разів за вказаний період (з дати F по дату T)
-- Нехай С = Sonny Prigmore (id = 6), N = 2, F = 2020-09-02, T = 2021-04-28

SELECT friend_id, name FROM rent JOIN rent_friends AS rf ON rent.rent_id = rf.rent_id JOIN friend ON 
rf.friend_id = friend.id
WHERE user_id = 6 and date('2021-04-28') > date and date > date('2020-09-02')
GROUP BY friend_id, name
HAVING COUNT(friend_id) >= 2;

-- 2. Для найманого друга X знайти усіх клієнтів, які наймали його принаймні N разів за вказаний період (з дати F по дату T)
-- Нехай X = Joela Feeley (id = 10), N = 1, F = 2020-09-02, T = 2021-04-28

SELECT user_id, name FROM rent JOIN rent_friends ON rent.rent_id = rent_friends.rent_id JOIN user_ ON rent.user_id = user_.id
WHERE friend_id = 10 and date('2021-04-28') > date and date > date('2020-09-02')
GROUP BY user_id, name
HAVING COUNT(user_id) >= 1;

-- 3. Для найманого друга X знайти усі свята, на які його наймали принаймні N разів за вказаний період (з дати F по дату T)
-- Нехай X = Joe Crosetti (id = 5), N = 1, F = 2020-09-02, T = 2021-04-28

SELECT party.party_id, name AS party_name FROM rent JOIN rent_friends ON rent.rent_id = rent_friends.rent_id JOIN party ON rent.party_id = party.party_id
WHERE friend_id = 5 and date('2021-04-28') > date and date > date('2020-09-02')
GROUP BY party.party_id, name
HAVING COUNT(party.party_id) >= 2;

-- 4. Знайти усiх клiєнтiв, якi наймали щонайменше N рiзних друзiв за вказаний перiод (з дати F по дату T);
-- Нехай N = 2, F = 2020-09-02, T = 2021-04-28

SELECT * FROM rent JOIN rent_friends ON rent.rent_id = rent_friends.rent_id JOIN user_ ON rent.user_id = user_.id
	WHERE date('2021-04-28') > date and date > date('2020-09-02')
	GROUP BY user_id, friend_id
	HAVING COUNT(user_id) >= 2;


-- 5.  знайти усiх найманих друзiв, яких наймали хоча б N разiв за вказаний перiод (з дати F по
-- дату T);
SELECT friend_id FROM rent JOIN rent_friends on rent.rent_id = rent_friends.rent_id
	WHERE  date('2012-01-08') > date and date > date('1999-01-08')
	GROUP BY friend_id
	HAVING COUNT(friend_id) > 3;

-- 6. знайти сумарну кiлькiсть побачень по мiсяцях;
SELECT COUNT(DATE_TRUNC('month',date)) as dates_for_months
FROM rent
GROUP BY DATE_TRUNC('month',date);

-- 7. для найманого друга Х та кожного свята, на якому вiн побував,
-- знайти скiльки разiв за вказаний перiод (з дати F по дату T) вiн був найнятий
-- на свято у групi з принаймнi N друзiв;
SELECT COUNT(*) FROM (
	SELECT DISTINCT rent_id FROM (
		SELECT rent_id, friend_id AS x_id FROM friend 
		JOIN rent_friends ON friend.id = rent_friends.friend_id
		JOIN rent USING (rent_id)
		WHERE friend_id = 10 AND party_id IS NOT NULL AND date BETWEEN date('2020-09-02') AND date('2021-04-28')
	) AS filtered_parties
	JOIN rent_friends USING (rent_id)
	GROUP BY rent_id
	HAVING COUNT(rent_id) >= 2
) AS groups;

-- 8. вивести подарунки у порядку спадання середньої кiлькостi вихiдних,
-- що брали найманi друзi, якi отримували подарунок вiд клiєнта С протягом 
-- вказаного перiоду (з дати F по дату T);

SELECT present_id FROM present_given
LEFT JOIN dayoffs USING (friend_id)
WHERE user_id = 6 AND present_given.date BETWEEN date('2001-09-02') AND date('2030-04-28')
GROUP BY present_id
ORDER BY COUNT(DISTINCT dayoffs.date) DESC;

-- 10. знайти усi спiльнi подiї для клiєнта С та найманого
-- друга Х за вказаний перiод (з дати F по дату T);
SELECT rent_id FROM rent 
JOIN rent_friends USING (rent_id)
WHERE user_id = 6 AND friend_id = 5 AND date BETWEEN date('2001-09-02') AND date('2030-04-28');


-- 11. знайти усi днi коли вихiдними були вiд А до В найманих друзiв, включно;
SELECT date FROM dayoffs
GROUP BY date
HAVING COUNT(date) BETWEEN 2 AND 3;

-- 12. по мiсяцях знайти середню кiлькiсть клiєнтiв у групi,
-- що реєстрували скаргу на найманого друга Х;



