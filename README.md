# Under Repair Middleware

A simple django **middleware** to show another page when site is under repair

## Installation

0. clone this repo `$ git clone `
1. copy `under_repair` package alongside your other apps
2. add `under_repair` to your `INSTALLED_APPS` in `settings.py`

```python

INSTALLED_APPS = [
    ...,
    "under_repair",
    ...,
]

```

3. add `under_repair.middleware.UnderRepairMiddleware` to the very first of your `MIDDLEWARE`

```python
MIDDLEWARE = [
    "under_repair.middleware.UnderRepairMiddleware",
    # other middlewares
    ...,
]

```

4. Done :)

## Configuration

By default, this middleware is deactivated. You can **activate** or **deactivate** this middleware from `settings.py` module

#### config sample

Put below lines to your project `settings.py` module

```python
UNDER_REPAIR = {
    "ACTIVATE": True,
}

```

# Customization

You can create your own view to show to the users.

##### Important

- If you wanna add `JavaScript` to your template, put it inside the HTML. Because, `under_repair` middleware doesn't support static files for now. May be in the future
- It's only accept **Function Based Views**, class based will be add in future

```python
UNDER_REPAIR = {
    "ACTIVATE": True,
    "VIEW": "APP_NAME.views.YOUR_VIEW_FUNCTION",
}

```

---

## Next Changes

These are some idea for my self and who wants contribute to project

- Creating a model to store `activate` status of middleware
- Adding the support of `static files`
- Creating good default UI (I don't like frontend, help me :))
