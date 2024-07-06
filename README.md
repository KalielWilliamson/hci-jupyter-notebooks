
## To Create the Heroku App:
```bash
heroku login
heroku create hci-jupyter-notebooks
```
## To Deploy The Heroku App
1. Log Into Heroku Container Registry:
```bash
heroku container:login
```

2. Make sure to have heroku-postgresql addon
```bash
heroku addons:create heroku-postgresql:essential-0 -a hci-jupyter-notebooks
````

2. Build and Push Docker Image:
```bash
heroku container:push web -a hci-jupyter-notebooks
```

3. Release the Docker Image
```bash
heroku container:release web -a hci-jupyter-notebooks
```

4. Open The App
```bash
heroku open -a hci-jupyter-notebooks 
```

5. View The Logs
```bash
heroku logs --tail -a hci-jupyter-notebooks
```

## One Liner
```bash
heroku container:push web -a hci-jupyter-notebooks && heroku container:release web -a hci-jupyter-notebooks && heroku open -a hci-jupyter-notebooks && heroku logs --tail -a hci-jupyter-notebooks
```
