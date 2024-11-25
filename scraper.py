
import instaloader
import re

# Create an Instaloader instance
L = instaloader.Instaloader()

# Input Instagram login credentials
username = input("Enter your Instagram username: ")
password = input("Enter your Instagram password: ")

# Login
try:
    L.login(username, password)
    print("Login successful!")
except Exception as e:
    print(f"Error logging in: {e}")
    exit()

# Input target Instagram profile
target_profile = input("Enter the target Instagram profile (username): ")

# Load profile
try:
    profile = instaloader.Profile.from_username(L.context, target_profile)
except Exception as e:
    print(f"Error loading profile: {e}")
    exit()

# Profile details
print(f"\n--- Profile Details of {target_profile} ---")
print(f"Username: {profile.username}")
print(f"Full Name: {profile.full_name}")
print(f"Bio: {profile.biography}")
print(f"Followers: {profile.followers}")
print(f"Following: {profile.followees}")
print(f"Posts: {profile.mediacount}")

# Attempt to extract email from the bio if it exists
email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', profile.biography)
if email_match:
    print(f"Email found in bio: {email_match.group(0)}")
else:
    print("No email found in bio.")

# Download posts, reels, and stories
download_choice = input("\nDo you want to download posts, reels, and stories? (yes/no): ").lower()

if download_choice == 'yes':
    try:
        # Download all posts (including photos, videos, and reels)
        print("\nDownloading posts...")
        for post in profile.get_posts():
            L.download_post(post, target=profile.username)

        # Download stories (if available)
        print("\nDownloading stories...")
        try:
            if profile.has_viewable_story:
                for story in L.get_stories([profile.userid]):
                    for item in story.get_items():
                        L.download_storyitem(item, target=profile.username + '_stories')
                print("Stories download complete!")
            else:
                print("No stories are currently available.")
        except Exception as e:
            print(f"Error downloading stories: {e}")

        print("\nDownload complete!")
    except Exception as e:
        print(f"Error downloading content: {e}")
else:
    print("Download skipped.")
