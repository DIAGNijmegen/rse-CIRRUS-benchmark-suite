import os

from cirrus_benchmark_suite.utils import DEBUG, getenv


def _manual_user_login(page):
    print("Performing manual login")
    page.get_by_text("Successfully signed in as").wait_for(
        timeout=120_000,  # 2 minutes
    )


def _automatic_user_login(page, username, password):
    page.get_by_placeholder("Username or email").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Sign In").click()
    page.get_by_text("Successfully signed in as").wait_for()


def login(page):
    page.goto("https://grand-challenge.org/accounts/login/")
    try:
        username = getenv("GRAND_CHALLENGE_USERNAME")
        password = getenv("GRAND_CHALLENGE_PASSWORD")
    except ValueError as e:
        if DEBUG:
            _manual_user_login(page)
        else:
            raise e
    else:
        _automatic_user_login(page, username, password)


def create_viewer_session(page):
    session_create_url = os.getenv(
        "SESSION_CREATE_URL",
        "https://grand-challenge.org/viewers/cirrus-staging/sessions/create/",
    )

    response = page.goto(session_create_url)

    if response.status in (404, 403):
        raise RuntimeError(
            f"Failed to create the viewer session. Either there is no active image for the viewer or insufficient permissions. URL used: {session_create_url}"
        )

    assert response.ok, "session creation started"
    page.wait_for_url("**/cirrus/", timeout=30_000)

    return page.url


permission_checks = []


def permission_check(url):
    def decorator(func):
        permission_checks.append(url)

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


def do_permission_checks(page):
    problem_urls = []
    for url in permission_checks:
        response = page.goto(url)
        if not response.ok:
            problem_urls.append(url)
    if problem_urls:
        raise RuntimeError(
            f"Insufficient permissions for URLs: {problem_urls}"
        )
