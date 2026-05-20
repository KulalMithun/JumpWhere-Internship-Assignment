def containsNearbyDuplicate(nums, k):
    window = set()
    for i in range(len(nums)):
        if nums[i] in window:
            return True
        window.add(nums[i])
        if len(window) > k:
            window.remove(nums[i-k])
    return False

print(containsNearbyDuplicate([99,99], 2))
