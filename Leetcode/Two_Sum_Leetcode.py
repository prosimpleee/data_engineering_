class Solution(object):
    def twoSum(self, nums, target):
        for i in range(len(nums) - 1):
            for k in range(i+1, len(nums)):
                if nums[i] + nums[k] == target:
                    return [i, k]

