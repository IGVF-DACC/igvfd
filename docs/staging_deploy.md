1. Clean up `igvfd` JIRA release
    * Make sure all tickets merged to `dev` branch

2. Evaluate the changes on `dev` vs. `main`, and decide if the changes grant minor (non-breaking) or major (breaking) version update

3. Make a branch to update the version number to `X.Y.Z` in `igvfd/src/igvfd/__init__.py` push and make PR

4. After approval and merge of the version update branch to `dev` create PR from `dev` to `main` branch

5. After approval of the PR to `main` follow next steps

6. Merge the PR to `main`.
```
$ git checkout dev
$ git fetch origin -p
$ git pull
$ git checkout main
$ git pull
$ git merge dev --ff-only

proceed ONLY if no merge conflicts/errors encountered!

$ git push origin main
```

7. This will cause the `staging` to be updated

8. Copy the list of commits that have been merged to `main`:
```
$ git checkout main
$ git fetch origin -p
$ git pull
$ git log --pretty
```

9. After choosing the commits to be included in the tag. Make the tag for version `X.Y.Z`:
```
$ git checkout dev
$ git tag -a vX.Y.Z # Add vX.Y.Z to details
$ git push origin tags/vX.Y.Z
```

10. On Github `Make a Release` from the tag, pasting the proper commits in the details.
