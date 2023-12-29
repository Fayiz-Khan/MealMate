#importing the necessary libraries
import openai
openai.api_key = "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"


#function to prompt the user to input their information and return those values
def get_user_info():
    current_weight = int(input("What is your current weight in pounds? "))
    goal_weight = int(input("What is your goal weight in pounds? "))
    height = float(input("What is your height in inches? "))
    age = int(input("What is your age in years? "))
    weekly_goal = int(input("How many pounds would you like to lose/gain per week? "))
    return current_weight, goal_weight, height, age, weekly_goal


#function thatcalculates the daily caloric intake required for the user to achieve
#their goal weight, based on their personal information and weekly weight loss/gain goal.
def calculate_daily_calories(current_weight, goal_weight, height, age, weekly_goal):
    # Calculate daily caloric intake required to achieve goal weight
    if goal_weight > current_weight:
        daily_calories = (10 * current_weight + 6.25 * height - 5 * age + 5) * 1.2
    else:
        daily_calories = (10 * current_weight + 6.25 * height - 5 * age - 161) * 1.2
    daily_calories += weekly_goal * 500 # Add calories to gain or subtract to lose weight based on weekly_goal
    return daily_calories


#function uses OpenAI's GPT-3 model to generate a meal and workout plan based on
#the user's daily caloric intake. The function formats the output to include the calories for each meal.
def generate_meal_and_workout_plan(daily_calories):
    # Generate meal and workout plan using OpenAI's GPT-3
    prompt = f"Generate a meal and five day workout plan with approximately {daily_calories} calories per day."
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=2048,
      n=1,
      stop=None,
      temperature=0.5,
    )
    #
    output = response.choices[0].text
    output = output.replace('\n\n', '\n').strip() # Remove extra newlines and whitespace
    sections = output.split('\n\n')
    meal_plan = ""
    workout_plan = ""
    for section in sections:
        if "Meal Plan:" in section:
            meal_plan = section.replace('Meal Plan:', '').strip()
            meal_plan = meal_plan.replace('Breakfast:', 'Breakfast ({0} calories):'.format(int(daily_calories * 0.25)))
            meal_plan = meal_plan.replace('Lunch:', 'Lunch ({0} calories):'.format(int(daily_calories * 0.35)))
            meal_plan = meal_plan.replace('Dinner:', 'Dinner ({0} calories):'.format(int(daily_calories * 0.35)))
            meal_plan = meal_plan.replace('Snack:', 'Snack ({0} calories):'.format(int(daily_calories * 0.05)))
        elif "Workout Plan:" in section:
            workout_plan = section.replace('Workout Plan:', '').strip()
    return meal_plan, workout_plan


# Get user information
current_weight, goal_weight, height, age, weekly_goal = get_user_info()
# Calculate required daily caloric intake
daily_calories = calculate_daily_calories(current_weight, goal_weight, height, age, weekly_goal)
print("Your required daily caloric intake is {0} calories per day.".format(int(daily_calories)))
# Generate meal and workout plan
meal_plan, workout_plan = generate_meal_and_workout_plan(daily_calories)
print("\n\nMeal Plan:")
print(meal_plan)
print("Workout Plan:")
print(workout_plan)
