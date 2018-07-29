function clip(v, min, max)
    if v < min then
        return min
    elseif v > max then
        return max
    else
        return v
    end
end

previous_bubbles = 0
function correct_bubbles()
  if done_check() then
    return -10
  end
  if data.bubbles > previous_bubbles then
    local delta = data.bubbles - previous_bubbles
    previous_bubbles = data.bubbles
    return delta
  else
    return 0
  end
end

function done_check()
  if data.gameover == 0 then
    return true
  end
  return false
end

previous_score = 0
death_score = -750
clip_min = -1000
clip_max = 1000

function correct_score ()
  local delta = 0
  if done_check() then
    --penalty for dieing
    delta = death_score
  else
    local current_score = 0
    local tens = (data.score_jyuu / 16) * 10
    local hundreds = (data.score_hyaku % 16)*100
    local thousands = (math.floor(data.score_hyaku/16))*1000
    local ten_thousands = (data.score_man % 16)*10000
    local hundred_thousands = (math.floor(data.score_man/16))*100000
    current_score = tens + hundreds + thousands + ten_thousands + hundred_thousands

    if current_score > previous_score then
      delta = current_score - previous_score
      previous_score = current_score
      if delta == 50 then
        delta = 0 --no reward for wall bounces
      end
    elseif previous_score - current_score > 500000 then
      --not sure what happens when you get over 1,000,000. if it resets then this catches it
      delta = 1000000 - previous_score + current_score
      previous_score = current_score
    end
  end

  delta = clip(delta, clip_min, clip_max)
  return delta
end
