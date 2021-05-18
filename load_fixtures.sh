MIGRATIONS_DIR=/rareapi/__migrations__

echo "Checking for migrations"
if [ -d "$MIGRATIONS_DIR" ]
then
    echo "Directory Deleting migrations directory"
    rm -rf /rareapi/__migrations__
else
    echo "Migrations directed already deleted"
fi

echo "Running migrate on User"
python3 manage.py migrate

echo "Running makemigrations and migrate on app"
python3 manage.py makemigrations rareapi
python3 manage.py migrate

echo "Loading fixtures"
python3 manage.py loaddata users
python3 manage.py loaddata rareuser
python3 manage.py loaddata tokens
python3 manage.py loaddata demotionqueue
python3 manage.py loaddata subscriptions
python3 manage.py loaddata tags
python3 manage.py loaddata categories
python3 manage.py loaddata reactions
python3 manage.py loaddata posts
python3 manage.py loaddata posttags
python3 manage.py loaddata comments
python3 manage.py loaddata postreactions

echo "Running Server"
python3 manage.py runserver
