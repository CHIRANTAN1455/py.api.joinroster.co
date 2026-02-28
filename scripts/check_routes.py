#!/usr/bin/env python3
"""
Compare Laravel api.php routes with FastAPI routes.
Run from project root: python3 scripts/check_routes.py
"""
import re
import sys

# Add project root to path
sys.path.insert(0, ".")


def normalize_path(path: str) -> str:
    """Convert path to comparable form (param names normalized)."""
    return re.sub(r"\{[^}]+\}", "{param}", path)


# Laravel api.php routes: (method, path) — path is relative to /api
LARAVEL_API_ROUTES = [
    ("POST", "/auth/init"),
    ("POST", "/auth/login"),
    ("POST", "/auth/social"),
    ("POST", "/auth/register"),
    ("POST", "/auth/reset"),
    ("POST", "/auth/new-password"),
    ("POST", "/auth/linkedin"),
    ("POST", "/auth/otp/reset"),
    ("POST", "/auth/otp/verify"),
    ("POST", "/auth/otp"),
    ("POST", "/auth/verify"),
    ("GET", "/auth/chat"),
    ("POST", "/auth/logout"),
    ("POST", "/auth/password"),
    ("POST", "/auth/broadcasting"),
    ("GET", "/profile"),
    ("GET", "/profile/statistics"),
    ("GET", "/profile/social"),
    ("POST", "/profile/update"),
    ("POST", "/profile/pricing"),
    ("POST", "/profile/pricing/no-delete"),
    ("POST", "/profile/skills"),
    ("POST", "/profile/jobtypes"),
    ("POST", "/profile/contentverticals"),
    ("POST", "/profile/contentverticals/new"),
    ("POST", "/profile/platforms"),
    ("POST", "/profile/softwares"),
    ("POST", "/profile/equipments"),
    ("POST", "/profile/creativestyles"),
    ("POST", "/customer/register"),
    ("POST", "/customer/sendgrid/webhook"),
    ("GET", "/customer/by-user"),
    ("POST", "/customer/upgrade"),
    ("GET", "/customer/billing"),
    ("GET", "/userproject/public/info"),
    ("GET", "/userproject/public"),
    ("GET", "/userproject"),
    ("GET", "/userproject/info"),
    ("POST", "/userproject"),
    ("POST", "/userproject/{id}/update"),
    ("DELETE", "/userproject/{id}"),
    ("GET", "/usercreator"),
    ("GET", "/usercreator/unverified"),
    ("GET", "/usercreator/content-topics"),
    ("GET", "/usercreator/search"),
    ("GET", "/usercreator/similar"),
    ("POST", "/usercreator"),
    ("GET", "/usercreator/info"),
    ("GET", "/usercreator/{id}/projects"),
    ("POST", "/usercreator/{id}/update"),
    ("DELETE", "/usercreator/{id}"),
    ("POST", "/usercreator/colleauges/invite"),
    ("POST", "/usercreator/group/add"),
    ("GET", "/usercreator/public/info"),
    ("GET", "/usercreator/search/public"),
    ("GET", "/usercreator/public/{username}"),
    ("GET", "/skills"),
    ("GET", "/skills/get"),
    ("GET", "/contentverticals"),
    ("GET", "/contentverticals/get"),
    ("GET", "/platforms"),
    ("GET", "/platforms/get"),
    ("GET", "/softwares"),
    ("GET", "/softwares/get"),
    ("GET", "/equipments"),
    ("GET", "/equipments/get"),
    ("GET", "/creativestyles"),
    ("GET", "/creativestyles/get"),
    ("GET", "/contentforms"),
    ("GET", "/contentforms/get"),
    ("GET", "/projecttypes"),
    ("GET", "/projecttypes/{username}"),
    ("GET", "/projecttypes/get"),
    ("GET", "/jobtypes"),
    ("GET", "/jobtypes/get"),
    ("GET", "/reasons"),
    ("GET", "/reasons/get"),
    ("GET", "/referrals"),
    ("GET", "/referrals/get"),
    ("GET", "/editor"),
    ("POST", "/editor"),
    ("PUT", "/editor"),
    ("PATCH", "/editor"),
    ("DELETE", "/editor"),
    ("GET", "/editor/{id}"),
    ("GET", "/editor/metadata/{id}"),
    ("GET", "/editor/{id}/projects"),
    ("GET", "/editor/{id}/creators"),
    ("GET", "/editor/{id}/jobtypes"),
    ("GET", "/editor/{id}/reviews"),
    ("POST", "/editor/store"),
    ("POST", "/editor/admin/reset-password"),
    ("POST", "/editor/email/{id}"),
    ("POST", "/editor/profile/bulk-email/{id}"),
    ("GET", "/editor/{id}/related"),
    ("GET", "/favourite"),
    ("POST", "/favourite"),
    ("GET", "/matching"),
    ("GET", "/matching/project/{id}"),
    ("PATCH", "/matching/editor"),
    ("POST", "/public-matching"),
    ("GET", "/matching/{id}"),
    ("GET", "/matching/token/{token}"),
    ("POST", "/matching"),
    ("POST", "/matching/creators"),
    ("PATCH", "/matching/{id}"),
    ("PATCH", "/matching/admin/{id}"),
    ("GET", "/admin/editors"),
    ("GET", "/admin/editors/{id}"),
    ("GET", "/admin/creators/{id}"),
    ("GET", "/admin/creators"),
    ("GET", "/admin/projects"),
    ("GET", "/admin/projects/{id}"),
    ("DELETE", "/admin/editors/{email}"),
    ("POST", "/admin/users/email"),
    ("POST", "/file"),
    ("GET", "/social"),
    ("GET", "/profile/social/content-topics"),
    ("POST", "/social"),
    ("DELETE", "/social/{id}"),
    ("GET", "/payment"),
    ("POST", "/payment"),
    ("DELETE", "/payment/{id}"),
    ("POST", "/data/editor"),
    ("POST", "/data/country"),
    ("POST", "/data/state"),
    ("POST", "/data/city"),
    ("POST", "/data/location"),
    ("POST", "/data/editor/invite"),
    ("GET", "/location"),
    ("GET", "/location/{id}"),
    ("GET", "/project/public/metadata/{id}/no-auth"),
    ("GET", "/project/public/{id}/no-auth"),
    ("GET", "/project/hackathon/{id}/no-auth"),
    ("GET", "/project/public/no-auth"),
    ("GET", "/project/hackathon/{id}"),
    ("GET", "/project"),
    ("GET", "/project/match-score"),
    ("POST", "/project/alert"),
    ("POST", "/project/alerts/2-days"),
    ("GET", "/project/public"),
    ("POST", "/project/add"),
    ("POST", "/project/public/add"),
    ("PATCH", "/project/{id}"),
    ("PATCH", "/project/public/{id}"),
    ("GET", "/project/{id}"),
    ("GET", "/project/public/{id}"),
    ("POST", "/project/hackathon/public/{id}"),
    ("POST", "/project/{id}/cancel"),
    ("POST", "/project/{id}/response"),
    ("POST", "/project/{id}/status"),
    ("POST", "/project/{id}/milestone"),
    ("POST", "/project/{id}/deposit"),
    ("POST", "/project/{id}/purchase"),
    ("POST", "/project/{id}/review"),
    ("POST", "/project/{id}/feedback"),
    ("GET", "/project/{id}/conversation"),
    ("GET", "/project/{projectUuid}/screening-questions"),
    ("POST", "/project/{projectUuid}/screening-questions"),
    ("GET", "/project/{projectUuid}/screening-questions/{questionUuid}"),
    ("PATCH", "/project/{projectUuid}/screening-questions/{questionUuid}"),
    ("DELETE", "/project/{projectUuid}/screening-questions/{questionUuid}"),
    ("GET", "/project-application"),
    ("GET", "/project-application/{id}"),
    ("POST", "/project-application/add"),
    ("PATCH", "/project-application/{id}"),
    ("POST", "/project-application/{id}/note"),
    ("DELETE", "/project-application/note/{id}"),
    ("POST", "/project-application/rejection"),
    ("GET", "/chat"),
    ("GET", "/chat/received_messages"),
    ("POST", "/chat/init/public"),
    ("POST", "/chat/init"),
    ("GET", "/chat/{id}"),
    ("POST", "/chat/{id}"),
    ("POST", "/chat/admin/custom"),
    ("PATCH", "/chat/message/{id}"),
    ("GET", "/questionnaire/{id}"),
    ("POST", "/questionnaire/add"),
    ("POST", "/callback/stripe"),
    ("POST", "/callback/post-transaction/slack"),
    ("POST", "/callback/post-transaction/email"),
    ("POST", "/callback/webflow"),
    ("GET", "/userverification"),
    ("POST", "/userverification"),
    ("POST", "/userverification/many"),
    ("DELETE", "/userverification/{id}"),
    ("POST", "/user/{id}/slack"),
    ("PATCH", "/user/{id}"),
    ("PATCH", "/user/{id}/timezone"),
    ("POST", "/user/{id}/jobtypes"),
    ("POST", "/user/{id}/content-vertical"),
    ("POST", "/user/{id}/platforms"),
    ("POST", "/user/{id}/revert-update-time"),
    ("POST", "/user/{id}/policy-acceptance"),
    ("DELETE", "/user/{id}"),
    ("GET", "/user/referral/{code}"),
    ("POST", "/user/notifications/{id}"),
    ("POST", "/profile-visit"),
    ("GET", "/referral-records"),
    ("GET", "/referral-paid-records"),
    ("GET", "/shortlist"),
    ("PATCH", "/shortlist/{id}"),
    ("DELETE", "/shortlist/{id}"),
    ("POST", "/upload"),
    ("POST", "/upload/multiple"),
    ("GET", "/user-to-do"),
    ("POST", "/user-to-do"),
    ("PATCH", "/user-to-do/{id}"),
    ("DELETE", "/user-to-do/{id}"),
    ("PATCH", "/job-posting/edit/{uuid}"),
    ("PATCH", "/pdfsend"),
    ("GET", "/users/metrics"),
    ("GET", "/public-job-listing"),
    ("PATCH", "/freejobpost"),
]


def get_fastapi_routes():
    from main import app
    routes = []
    for r in app.routes:
        if hasattr(r, "methods") and hasattr(r, "path"):
            path = r.path
            if path.startswith("/api"):
                path = path[4:] or "/"
            if not path.startswith("/"):
                path = "/" + path
            for method in r.methods:
                if method.upper() != "HEAD":
                    routes.append((method.upper(), path))
    return routes


def main():
    fastapi_routes = get_fastapi_routes()
    laravel_set = set()
    for method, path in LARAVEL_API_ROUTES:
        p = path if path.startswith("/") else "/" + path
        laravel_set.add((method, normalize_path(p)))
    fastapi_set = set()
    skip_paths = {"/docs", "/redoc", "/openapi.json", "/docs/oauth2-redirect", "/health/db"}
    for method, path in fastapi_routes:
        if path in skip_paths:
            continue
        fastapi_set.add((method, normalize_path(path)))
    missing = laravel_set - fastapi_set
    extra = fastapi_set - laravel_set
    print("=== Laravel api.php vs FastAPI route check ===\n")
    print(f"Laravel routes (normalized): {len(laravel_set)}")
    print(f"FastAPI routes (normalized): {len(fastapi_set)}")
    if missing:
        print(f"\n*** MISSING IN FASTAPI ({len(missing)}): ***")
        for m, p in sorted(missing):
            print(f"  {m:6} {p}")
    if extra:
        print(f"\n*** EXTRA IN FASTAPI (not in Laravel) ({len(extra)}): ***")
        for m, p in sorted(extra):
            print(f"  {m:6} {p}")
    if not missing:
        print("\nAll Laravel api.php routes have a matching FastAPI route.")
    return 0 if not missing else 1


if __name__ == "__main__":
    exit(main())
