# How to contribute to thingbooker 🥳

## I found a bug

If you find a bug that affects security, please do not submit an issue. Please write a mail to [erlendskaaden(at)gmail.com](mailto:erlendskaaden@gmail.com)
where you explain the issue.

If you find a bug that does not affect security, first check if there is a similar bug report in the
[issues list](https://github.com/erlendps/thingbooker/issues). If you cannot find anything similar, please submit a issue. In the issue, please:

- Write a short and concise title
- Describe what the bug is
  - How to reproduce it
  - What happend?
  - What did you expect should happen?
- Label the issue with the "bug" label

## I have an idea to make thingbooker better

First consult the [issues list](https://github.com/erlendps/thingbooker/issues) to check for duplicates. If there are no similar suggestions,
please submit an issue. When writing the issue, please:

- Write a short and concise title
- Describe the problem you want to solve
  - What
  - Why, i.e name a use case
- Label the issue with the "enhancement" label

## I want to write code!

Firstly, find a issue in the [issues list](https://github.com/erlendps/thingbooker/issues). When coding, please keep in mind the different conventions
we use:

- Please keep commits to a single "thing", i.e a single commit shouldn't touch upon two separate things.
- commits should be prefixed by a tag
  - `backend:` if the commit modifies backend code
  - `frontend:` if the commit modifies frontend code
  - `conf:` if the commit modifies configuration files in the root directory
  - `deps:` if you are modifying dependencies
- Commit messages should be written in imperative
  - It should described what is changed in short, i.e __This commit will__ **implement filter in backend api**
- When you're finished, please tidy the commit history by interactively rebasing, if necessary, then open a pull request
- The pull request title should tell what is solved
- In the description, specify what the PR does in more detail, and why it is done. If there are UI changes, please add screenshots or videos.
- Wait for approval

Also, you should take care to try and follow the code style already implemented.
