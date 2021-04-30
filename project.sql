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
	  REFERENCES friend(friend_id)
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
	"name" varchar(40),
	"price" money,
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

-- знайти усiх клiєнтiв, якi наймали щонайменше N рiзних друзiв за вказаний перiод (з дати
-- F по дату T);
SELECT user_id FROM rent
	WHERE  date('2012-01-08') > date and date > date('1999-01-08')
	GROUP BY user_id
	HAVING COUNT(user_id) > 3;


--  знайти усiх найманих друзiв, яких наймали хоча б N разiв за вказаний перiод (з дати F по
-- дату T);
SELECT friend_id FROM rent JOIN rent_friends on rent.rent_id = rent_friends.rent_id
	WHERE  date('2012-01-08') > date and date > date('1999-01-08')
	GROUP BY friend_id
	HAVING COUNT(friend_id) > 3;

-- знайти сумарну кiлькiсть побачень по мiсяцях;
SELECT COUNT(DATE_TRUNC('month',date)) as dates_for_months
FROM rent
GROUP BY DATE_TRUNC('month',date);
