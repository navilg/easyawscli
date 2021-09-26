# easyawscli

This python script will help manage/control AWS services from your terminal easily and faster with just small interactive command.

```pip install -r requirements.txt```

```python3 easyawscli.py```

And script will lead your way. 



#### Requirements

- Python v3.8.5 and above with pip
- AWS access key and secret with all required access.
- Command Terminal (Powershell/Command prompt for windows or SHELL for Linux or Mac)

Know how to create AWS access key here: https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys

Use policy [easyawscli-aws-policy.json](easyawscli-aws-policy.json) to create a new policy for easyawscli and 
add it to your user's permission.

### Note:

Pasting secret text in `Windows powershell` or `Command prompt` with `Shift+insert` or `ctrl+v` doesn't work.

Enable paste action with `ctrl+shift+v` in powershell and command prompt for that with --> Right click on title bar of PS or cmd prompt --> properties --> Options --> Check mark 'use ctrl+shift+c/v as copy/paste'
Bug link: https://bugs.python.org/issue37426


### Contribution Guidelines:

- Use conventional commit message

Format: `<type>(<scope>): <subject>`

`<scope>` is optional

Example

```
feat(lang): add polish language
^--^        ^-----------------^
|           |
|           +-> Summary in present tense.
|
+-------> Type: chore, docs, feat, fix, refactor, style, or test.
```

- `feat`: (new feature for the user, not a new feature for build script)
- `fix`: (bug fix for the user, not a fix to a build script)
- `docs`: (changes to the documentation)
- `style`: (formatting, missing semi colons, etc; no production code change)
- `refactor`: (refactoring production code, eg. renaming a variable)
- `test`: (adding missing tests, refactoring tests; no production code change)
- `chore`: (updating grunt tasks etc; no production code change)

References:

- https://www.conventionalcommits.org/
- https://seesparkbox.com/foundry/semantic_commit_messages
- http://karma-runner.github.io/1.0/dev/git-commit-msg.html