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

  if data.lives > prev_lives then
    prev_lives = data.lives
  elseif data.lives < prev_lives then
    --potential issue if you gain a life as you lose a life
    return true
  end

  return false
end


prev_score = 0
death_score = -1.0 * math.log(500)
level_clear_bonus = math.log(100000)
clip_min = -15
clip_max = 15
existence_penalty = -1.0 * math.log(1.001) --life is suffering

function correct_score()
  local delta = existence_penalty
  if done_check() then
    if level ~= data.level then
      delta = delta + level_clear_bonus
    else
      --penalty for dieing
      delta = delta + death_score
    end
  else
    if data.score > prev_score then
      delta = delta + math.log(1+data.score-prev_score)
      prev_score = data.score
    elseif prev_score < data.score then
      --not sure if score ever resets, never really figured out the rom address to score calculation
      prev_score = data.score
    end
  end

  delta = clip(delta, clip_min, clip_max)
  return delta
end

