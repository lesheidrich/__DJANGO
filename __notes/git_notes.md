#### create and push
```
git init
git remote add origin git@github.com:username/repository.git
git add .
git commit -m "message"
git branch  // master or main
git push -u origin master

git status
git rm -r --cached path/to/file_or_directory
git checkout -b new-branch-name     // new branch   
git checkout branch-name            // switch
git merge branch-name
git pull origin branch-name
```

#### pull
```
git status
git fetch
git pull

git remote -v                 // ensure connected to right remote repo
git pull origin branch-name   // pull from specific branch
```