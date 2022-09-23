# Under Repair Middleware

A simple django **middleware** to show another page when site is under repair

## Installation

0. clone this repo `$ git clone https://github.com/mohamad-zahiry/under_repair.git`

1. copy **under_repair** package alongside your other apps

2. add **under_repair** to your `INSTALLED_APPS` in `settings.py`

```python

INSTALLED_APPS = [
    ...,
    "under_repair",
    ...,
]

```

3. add `under_repair.middleware.UnderRepairMiddleware` at the very first of your `MIDDLEWARE`

```python
MIDDLEWARE = [
    "under_repair.middleware.UnderRepairMiddleware",
    # other middlewares
    ...,
]

```

4. setup the `CACHES` in `settings.py`

```python

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 3600,  #  1 hour
    }
}
```

5. make the migrations

```shell
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

It's Done :)

## Configuration

The Rules(Configurations) are stored in a database table which named **UnderRepairRule** model. Each rule, has 4 fields:

- **description**: A short desctription about the rule
- **is_active**: Status of the rule
  Only 1 or zero rule can be active at the moment. This is handled by `UnderRepairRule.save` method.
- **admin_url**: The admin page url without protocol and www.
  e.g:

        yahoo.com/admin

  This url and subURLs are ignored by Under Repair Middleware. This is necessary because the website administrators need to login to admin panel in any situation.

- **view_path**: Absolute path to your view function.
  e.g:

        under_repair.views.under_repair_view

  This view must be a **Function Based View**. CBV support will be added.

## Customization

You can create your own **view** or **admin panel url**, or even, create some records with different views and admin panel urls for future and activate them as you need it.

##### Important

- If you wanna add `JavaScript` to your template(to show in under repair view/template), put it inside the HTML. Because, **under_repair** middleware doesn't support static files for now. May be in the future
- It's only accept **Function Based Views**, class based will be add in future

---

## Next Changes

These are some idea for my self and who wants contribute to project

- Refactoring the code (it could be better. I'm a junior :()
- Adding the support of `static files`
- Creating good default UI (I don't like frontend, help me :))
