import sys
import re

RULES = {
    'major': lambda m, d: (int(m[0])+(not d or -1), 0, 0, ''),
    'minor': lambda m, d: (int(m[0]), int(m[1])+(not d or -1), 0, ''),
    'patch': lambda m, d: (int(m[0]), int(m[1]), int(m[2])+(not d or -1), ''),
    'premajor': lambda m, d: (int(m[0])+(not d or -1), 0, 0, 'a0'),
    'preminor': lambda m, d: (int(m[0]), int(m[1])+(not d or -1), 0, 'a0'),
    'prepatch': lambda m, d: (int(m[0]), int(m[1]), int(m[2])+(not d or -1), 'a0'),
    'prerelease': lambda m, d: prerelease_bump(m, d),
}

def prerelease_bump(m, downgrade):
    major, minor, patch, pre = m
    major, minor, patch = int(major), int(minor), int(patch)
    
    if pre:
        tag, num = re.match(r'(\D+)(\d+)', pre).groups()
        num = int(num)
        
        if downgrade:
            if num > 0:
                # Normal prerelease downgrade
                return major, minor, patch, f'{tag}{num-1}'
            else:
                # If we're at x.y.za0, going down should reduce the patch level
                return major, minor, patch-1, ''
        else:
            # Normal prerelease increment
            return major, minor, patch, f'{tag}{num+1}'
    else:
        # For non-prerelease versions, increment the patch and add 'a0' or just increment/decrement normally
        if downgrade:
            return major, minor, patch-1, ''
        else:
            return major, minor, patch, 'a0'


def bump_version(current, rule, downgrade=False):
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)([a-z]\d+)?$', current)
    if not match:
        raise ValueError("Invalid version format")
    
    groups = match.groups()
    major, minor, patch, pre = RULES[rule](groups, downgrade)
    
    # Format the version string
    result = f"{major}.{minor}.{patch}"
    if pre:
        result += pre
    
    return result


def update_pyproject(rule='patch', downgrade=False):
    with open('pyproject.toml', 'r') as f:
        content = f.read()

    def replace_version(match):
        old_version = match.group(1)
        new_version = bump_version(old_version, rule, downgrade)
        print(f'Bumping version: {old_version} → {new_version}')
        return f'version = "{new_version}"'

    new_content, count = re.subn(r'version\s*=\s*"([^"]+)"', replace_version, content)

    if count == 0:
        raise ValueError("Version key not found in pyproject.toml")

    with open('pyproject.toml', 'w') as f:
        f.write(new_content)


if __name__ == '__main__':
    args = sys.argv[1:]
    rule = 'patch'
    downgrade = '--downgrade' in args

    if len(args) >= 2 and args[0] == 'version':
        rule = args[1]

    if rule not in RULES:
        print(f'Unknown rule: {rule}. Valid rules: {", ".join(RULES)}')
        sys.exit(1)

    update_pyproject(rule, downgrade)
