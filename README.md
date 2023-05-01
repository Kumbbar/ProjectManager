# ProjectManager
## Redmine clone


<image height="400" src="https://user-images.githubusercontent.com/90816195/235413963-bc73015b-12b1-43d3-8e7c-68bfc1d44819.png"/>

## Deployment

```
git clone https://github.com/Kumbbar/ProjectManager
cd ProjectManager
- Database and Debug
- vim project_manager/settings.py
cd ..
sudo docker-compose up
-- docker exec -it project_manager bash
-- python3 manage.py createsuperuser
-- python3 manage.py fill_statuses
```
