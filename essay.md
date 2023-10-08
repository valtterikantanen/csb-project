# Vulnerabilities

## 1. [A01:2021 – Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

Access control aims to ensure that users can only perform actions that they have permission for. In the current configuration of this application, any user can modify another user's book review, which clearly is a violation of access controls. This can lead to data tampering, loss of integrity, and user distrust. The attack is possible due to the fact that the backend does not check whether the user trying to edit a review is the same user who created the review.

Although the link to edit page is visible only to the review's creator, it is still possible to manually navigate to the page. The route follows the pattern `/reviews/<id>/edit`, making it straightforward to alter the id. This vulnerability is even easier to exploit since the ids are integers starting from 1 instead of unpredictable strings like UUIDs.

### Fix

The application must verify that the user trying to edit a review is the same user who created the review. This can be done by uncommenting the following lines in the `edit_review` function:

https://github.com/valtterikantanen/csb-project/blob/8ead83286535a9a2370c54bd7fb012d012d1aee6/src/pages/views.py#L109-L111

## 2. [A02:2021 – Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)

https://github.com/valtterikantanen/csb-project/blob/8ead83286535a9a2370c54bd7fb012d012d1aee6/src/pages/views.py#L23

https://github.com/valtterikantanen/csb-project/blob/8ead83286535a9a2370c54bd7fb012d012d1aee6/src/pages/views.py#L47-L48

Applications must guard sensitive data, including passwords, financial details, and personal information. This application stores passwords as plain text in its database. If an intruder gained access to this database, they would instantly obtain every user's password.

### Fix

Passwords should be stored as salted hashes rather than in plaintext. This transition can easily be accomplished through Django's built-in `make_password` function. By default, the function [uses](https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#how-django-stores-passwords) the PBKDF2 algorithm with a SHA256 hash. This makes it a lot harder for attackers to decipher the original passwords. Furthermore, in the event of a data breach, hashed passwords are of much less value to attackers than plaintext passwords.

This can be implemented by uncommenting the following line:

https://github.com/valtterikantanen/csb-project/blob/8ead83286535a9a2370c54bd7fb012d012d1aee6/src/pages/views.py#L46

Also, the `log_in` function will need modification to use the `check_password` function, given the changed manner of password storage. To do this, uncomment the lines 61 and 62 and comment out lines 60 and 63:

https://github.com/valtterikantanen/csb-project/blob/8ead83286535a9a2370c54bd7fb012d012d1aee6/src/pages/views.py#L60-L63

## 3. [A07:2021 – Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

Storing passwords in hashed form is only one part of the solution. Hashing does not protect against weak passwords. At the moment, the application does not enforce strong passwords. This means that users can create accounts with weak passwords such as "password" or "123456" which can be easily brute forced by attackers.

### Fix

Fortunately, Django provides a built-in password validator that can be used to enforce strong passwords. By default, four different validators [are used](/src/config/settings.py#L88-L101):

- `UserAttributeSimilarityValidator` ensures the password isn't overly similar to the username or other user attributes.
- `MinimumLengthValidator` checks that the password is at least 8 characters long.
- `CommonPasswordValidator` checks the password against the 1,000 most frequently used ones.
- `NumericPasswordValidator` checks that the password is not entirely numeric.

These validators can be taken into use by uncommenting the following lines in the `sign_up` function:

https://github.com/valtterikantanen/csb-project/blob/8ead83286535a9a2370c54bd7fb012d012d1aee6/src/pages/views.py#L31-L36

## 4. [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/)

https://github.com/valtterikantanen/csb-project/blob/8ead83286535a9a2370c54bd7fb012d012d1aee6/src/pages/views.py#L60

This application constructs an SQL query utilizing unsanitized user input. This vulnerability opens the door to SQL injection attacks. Such an attack allows malicious users to manipulate the application's SQL queries, possibly gaining unauthorized database access, revealing information, or even erasing data. As a result, an intruder could potentially log in using the username and password `" OR ""="`, even if such a username does not exist in the system.

Even though it would possibly be easier to create a new user and log in with that, this vulnerability is still a serious problem. Any logged in user can see the same data as there is no hidden data. However, if there were, an attacker could potentially gain access to that data.

### Fix

The most important rule to combat injection attacks is simple: never trust user input. To address this flaw, developers should prefer using parameterized queries or use the built-in query methods provided by Django. In this case, Django's ORM can be used to find the correct user without directly injecting user input into the SQL query. To do this, replace the line 60 (above) with the following:

```python
user = User.objects.filter(username=username, password=password).first()
```

## 5. [A06:2021 – Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)

https://github.com/valtterikantanen/csb-project/blob/8ead83286535a9a2370c54bd7fb012d012d1aee6/requirements.txt#L2

The application is currently running an obsolete Django version. This can be identified by executing `pip show django` after installing the dependencies from [`requirements.txt`](/requirements.txt). The currently used version, 4.2.5, [is vulnerable](https://github.com/django/django/blob/main/docs/releases/4.2.6.txt) to the CVE-2023-43665 vulnerability, categorized as "moderate" risk and potentially leading to a denial-of-service (DoS) attack.

### Fix

Just four days before writing this essay, version 4.2.6 was released, addressing the identified vulnerability. This highlights the crucial nature of regular dependency updates. Address this vulnerability by upgrading Django to the most recent version. This can be accomplished by running `pip install --upgrade django` inside the virtual environment.
