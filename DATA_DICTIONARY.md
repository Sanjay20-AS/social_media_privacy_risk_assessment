# Data Dictionary

The application uses 20 assessment controls.

| Field | Meaning | Risk direction |
|---|---|---|
| profile_visibility | Broad/public profile visibility | Yes = higher |
| personal_info | Public identifying details | Yes = higher |
| contact_info | Public phone/email | Yes = higher |
| location | Current/routine location exposure | Yes = higher |
| work_education | Detailed workplace/school exposure | Yes = higher |
| birthday | Full date of birth visibility | Yes = higher |
| family_relationships | Family/relationship exposure | Yes = higher |
| post_visibility | Broad post audience | Yes = higher |
| connection_controls | Unknown people accepted | Yes = higher |
| tagging | Unrestricted tagging | Yes = higher |
| third_party_apps | Unneeded app access | Yes = higher |
| authentication | Unique strong password | No = higher |
| mfa | MFA enabled | No = higher |
| password_reuse | Reused password | Yes = higher |
| login_alerts | Login/security alerts | No = higher |
| unknown_requests | Unknown requests accepted | Yes = higher |
| suspicious_links | Unexpected links clicked | Yes = higher |
| photo_metadata | Metadata awareness | No = higher |
| historical_posts | Old sensitive posts unaudited | No = higher |
| social_engineering | Public clues useful to social engineering | Yes = higher |

`unknown` receives a smaller exposure penalty because uncertainty itself can indicate that a user should review a setting, but it is not treated as equivalent to confirmed exposure.
