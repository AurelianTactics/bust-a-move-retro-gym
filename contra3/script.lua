function clip(v, min, max)
    if v < min then
        return min
    elseif v > max then
        return max
    else
        return v
    end
end

prev_lives = 0
level = data.level
function done_check()

  if level ~= data.level then
    return true
  end

  --if data.lives > prev_lives then
  --  prev_lives = data.lives
  --elseif data.lives < prev_lives then
    --potential issue if you gain a life as you lose a life
  --  return true
  --end

  if data.lives <= 0 then
    return true
  end

  return false
end


prev_score = 0
death_score = -.1 ---1.0 * math.log(10000)
level_clear_bonus = 100 --math.log(100000)
clip_min = -15
clip_max = 100
prev_lives_for_score = data.lives
death_frames_penalty = 30
death_frames_iter = 0

function correct_score()
  local delta = 0
  --print('score is ' .. data.score)
  if done_check() then
    if level ~= data.level then
      delta = delta + level_clear_bonus
    else
      --penalty for game over
      delta = delta + death_score
    end
    return delta
  elseif data.lives < prev_lives_for_score then
    prev_lives_for_score = data.lives
    delta = delta + death_score
    death_frames_iter = death_frames_penalty
  end

  --print('finding new score 1 ' .. data.score .. '  ' .. prev_score)
  if data.score > prev_score then
    delta = delta + math.log(1+data.score-prev_score)
    --print('finding new score 2')
  end
  --not sure if score ever resets, never really figured out the rom address to score calculation
  prev_score = data.score

  delta = scrollable_adjustment(delta)

  
  --penalty for death lasts for death_frames_penalty frames
  if death_frames_iter > 0 then
    death_frames_iter = death_frames_iter - 1
    delta = delta + death_score
  end

  delta = clip(delta, clip_min, clip_max)
  return delta
end

x_scroll_pos = 127 --player x position that enables level to scroll
x_scroll_constant = 1 --value that tells screen is horizontal scrollable
y_scroll_constant = 3 --value that tells screen is vert scrollable
scroll_reward = 0.05 --math.log(10)
scroll_multiplier = 0.0 --penalty for if level is scrollable and player is not progressing in level
existence_penalty = -1.0 * math.log(1.1) --life is suffering
prev_scroll_value = 0
prev_vert_scroll_value = 0

function scrollable_adjustment(r)
  
  if data.is_scrollable == x_scroll_constant then
    if data.scroll_value ~= prev_scroll_value then
      prev_scroll_value = data.scroll_value
      r = r + scroll_reward
    else
      --user position >= 127 to scroll
      --local distance_penalty = 0.
      --if data.x1 < x_scroll_pos then
      --  distance_penalty = -1 * math.log(1 + math.abs(x_scroll_pos-data.x1)/127.0) 
      --end
      r = clip(r,clip_min,scroll_reward*.5)--r -- scroll_multiplier --+ existence_penalty --+ distance_penalty
    end
  elseif data.is_scrollable == y_scroll_constant then
    if data.vert_scroll_value ~= prev_vert_scroll_value then
      --user data.x1 < 89 then goes up (but toggles between 89 and 90 as it goes up)
      prev_vert_scroll_value = data.vert_scroll_value
      r = r + scroll_reward
    else
      r = clip(r,clip_min,scroll_reward*.5) --r * scroll_multiplier --+ existence_penalty
    end
  else
    --print("in scrollable adjustment " .. r)
    r = r --+ existence_penalty
  end
  return r
end

