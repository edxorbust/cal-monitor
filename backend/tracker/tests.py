from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def payload(self):
        return {"username": "demo_tracker", "email": "demo@example.com",
                "password": "Example-tracker-726!", "password2": "Example-tracker-726!"}

    def test_register_login_refresh_and_me(self):
        payload = self.payload()
        response = self.client.post("/api/auth/register/", payload, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertNotIn("password", response.data)
        self.assertTrue(User.objects.get(username=payload["username"]).check_password(payload["password"]))
        login = self.client.post("/api/auth/token/", payload, format="json")
        self.assertEqual(login.status_code, 200, login.data)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + login.data["access"])
        me = self.client.get("/api/auth/me/")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.data["email"], payload["email"])
        refresh = self.client.post("/api/auth/token/refresh/", {"refresh": login.data["refresh"]}, format="json")
        self.assertEqual(refresh.status_code, 200, refresh.data)
        self.assertIn("access", refresh.data)

    def test_mismatched_passwords_do_not_create_user(self):
        payload = self.payload()
        payload["password2"] = "different"
        self.assertEqual(self.client.post("/api/auth/register/", payload, format="json").status_code, 400)
        self.assertFalse(User.objects.exists())

    def test_weak_password_is_rejected(self):
        payload = self.payload()
        payload.update(password="123", password2="123")
        self.assertEqual(self.client.post("/api/auth/register/", payload, format="json").status_code, 400)
        self.assertFalse(User.objects.exists())

    def test_duplicate_username_is_rejected(self):
        payload = self.payload()
        self.client.post("/api/auth/register/", payload, format="json")
        self.assertEqual(self.client.post("/api/auth/register/", payload, format="json").status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_private_routes_require_login(self):
        for path in ("/api/auth/me/", "/api/ingredients/", "/api/activities/", "/api/water/", "/api/summary/", "/api/profile/", "/api/meals/"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 401)

    def test_registration_ignores_stale_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer expired-token")
        response = self.client.post("/api/auth/register/", self.payload(), format="json")
        self.assertEqual(response.status_code, 201, response.data)

    def test_vite_origin_is_allowed(self):
        response = self.client.options("/api/auth/register/", HTTP_ORIGIN="http://localhost:5173",
                                       HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
                                       HTTP_ACCESS_CONTROL_REQUEST_HEADERS="content-type")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:5173")


class TrackerTests(APITestCase):
    def setUp(self):
        from .services import profile_for
        self.user = User.objects.create_user(username='alice', password='test')
        self.other = User.objects.create_user(username='bob', password='test')
        self.profile = profile_for(self.user)
        self.other_profile = profile_for(self.other)
        self.client.force_authenticate(self.user)

    def ingredient(self, name='Arroz', calories=130, portion=100):
        response = self.client.post('/api/ingredients/', {'name':name,'calories':calories,'portion_size':portion,'unit':'g'}, format='json')
        self.assertEqual(response.status_code, 201, response.data)
        return response.data

    def test_profile_is_created_for_existing_user_and_goals_persist(self):
        from .models import UserProfile
        self.profile.delete()
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['daily_calorie_goal'],2000)
        update = self.client.patch('/api/profile/', {'name':'Alice','weight':70.5,'height':170,'goal_weight':68,'daily_calorie_goal':2100,'water_goal_ml':2500,'is_creator':True,'user':self.other.id},format='json')
        self.assertEqual(update.status_code,200,update.data)
        self.assertEqual(self.client.get('/api/profile/').data['weight'],70.5)
        self.assertFalse(UserProfile.objects.get(user=self.user).is_creator)
        self.assertEqual(UserProfile.objects.get(user=self.other).daily_calorie_goal,2000)

    def test_calories_are_calculated_by_server_and_snapshot_is_preserved(self):
        first = self.ingredient()
        second = self.ingredient('Pollo',165)
        response = self.client.post('/api/meals/',{'name':'Almuerzo','calories':1,'ingredients':[{'ingredient':first['id'],'quantity':150},{'ingredient':second['id'],'quantity':100}]},format='json')
        self.assertEqual(response.status_code,201,response.data)
        self.assertEqual(response.data['calories'],360)
        meal_id=response.data['id']
        self.client.patch(f"/api/ingredients/{first['id']}/",{'calories':999},format='json')
        self.client.delete(f"/api/ingredients/{second['id']}/")
        detail=self.client.get(f'/api/meals/{meal_id}/').data
        self.assertEqual(detail['calories'],360)
        self.assertEqual(detail['items'][1]['name'],'Pollo')
        self.assertIsNone(detail['items'][1]['ingredient'])
        self.assertEqual(self.client.get('/api/summary/').data['consumed'],360)

    def test_daily_summary_date_filter_and_deletion(self):
        from django.utils import timezone
        from datetime import timedelta
        day=str(timezone.localdate())
        past=str(timezone.localdate()-timedelta(days=1))
        meal=self.client.post('/api/meals/',{'name':'Hoy','calories':500,'date':day},format='json')
        self.client.post('/api/meals/',{'name':'Ayer','calories':900,'date':past},format='json')
        self.client.post('/api/activities/',{'name':'Caminar','duration':30,'calories_burned':100,'date':day},format='json')
        water=self.client.post('/api/water/',{'amount':250,'date':day},format='json')
        self.client.post('/api/water/',{'amount':500,'date':day},format='json')
        summary=self.client.get('/api/summary/',{'date':day}).data
        self.assertEqual((summary['consumed'],summary['burned'],summary['net'],summary['remaining'],summary['water_ml']),(500,100,400,1600,750))
        self.assertEqual(self.client.get('/api/meals/',{'date':day}).data['count'],1)
        self.assertEqual(self.client.get('/api/summary/',{'date':past}).data['consumed'],900)
        self.client.delete(f"/api/meals/{meal.data['id']}/")
        self.client.delete(f"/api/water/{water.data['id']}/")
        summary=self.client.get('/api/summary/',{'date':day}).data
        self.assertEqual((summary['consumed'],summary['water_ml']),(0,500))

    def test_owners_cannot_read_change_or_delete_each_others_records(self):
        records=[]
        for path,payload in [('/ingredients/',{'name':'Arroz','calories':130,'portion_size':100,'unit':'g'}),('/meals/',{'name':'Comida','calories':400}),('/water/',{'amount':250}),('/activities/',{'name':'Correr','duration':30,'calories_burned':200})]:
            response=self.client.post('/api'+path,{**payload,'user_profile':self.other_profile.id},format='json')
            self.assertEqual(response.status_code,201,response.data)
            records.append((path,response.data['id']))
        self.client.force_authenticate(self.other)
        for path,pk in records:
            with self.subTest(path=path):
                self.assertEqual(self.client.get('/api'+path).data['count'],0)
                detail=f'/api{path}{pk}/'
                self.assertEqual(self.client.get(detail).status_code,404)
                self.assertEqual(self.client.patch(detail,{},format='json').status_code,404)
                self.assertEqual(self.client.delete(detail).status_code,404)
        self.assertEqual(self.client.get('/api/summary/').data['consumed'],0)
        self.assertEqual(self.client.get('/api/summary/').data['water_ml'],0)

    def test_foreign_ingredient_is_rejected_without_partial_meal(self):
        from .models import CalorieEntry
        ingredient=self.ingredient()
        self.client.force_authenticate(self.other)
        response=self.client.post('/api/meals/',{'name':'Invalid','ingredients':[{'ingredient':ingredient['id'],'quantity':50}]},format='json')
        self.assertEqual(response.status_code,400,response.data)
        self.assertEqual(CalorieEntry.objects.count(),0)

    def test_edit_meal_recalculates_and_manual_conversion_clears_items(self):
        ingredient=self.ingredient()
        meal=self.client.post('/api/meals/',{'name':'Meal','ingredients':[{'ingredient':ingredient['id'],'quantity':100}]},format='json').data
        path=f"/api/meals/{meal['id']}/"
        update=self.client.patch(path,{'ingredients':[{'ingredient':ingredient['id'],'quantity':200}]},format='json')
        self.assertEqual(update.status_code,200,update.data)
        self.assertEqual(update.data['calories'],260)
        self.assertEqual(len(update.data['items']),1)
        update=self.client.patch(path,{'ingredients':[],'calories':123},format='json')
        self.assertEqual(update.status_code,200,update.data)
        self.assertEqual(update.data['items'],[])
        self.assertEqual(update.data['calories'],123)

    def test_invalid_numbers_and_dates_return_validation_errors(self):
        for path,payload in [('/water/',{'amount':-1}),('/water/',{'amount':'NaN'}),('/ingredients/',{'name':'Bad','calories':5,'portion_size':0,'unit':'g'}),('/meals/',{'name':'Missing'}),('/meals/',{'name':'Negative','calories':-3}),('/activities/',{'name':'Bad','duration':0,'calories_burned':10}),('/meals/',{'name':'Bad','calories':10,'date':'invalid'})]:
            with self.subTest(path=path,payload=payload):
                self.assertEqual(self.client.post('/api'+path,payload,format='json').status_code,400)
        self.assertEqual(self.client.patch('/api/profile/',{'daily_calorie_goal':0},format='json').status_code,400)
        self.assertEqual(self.client.get('/api/summary/?date=invalid').status_code,400)

    def test_activity_update_changes_summary(self):
        entry=self.client.post('/api/activities/',{'name':'Walk','duration':30,'calories_burned':100},format='json').data
        response=self.client.patch(f"/api/activities/{entry['id']}/",{'duration':45,'calories_burned':150},format='json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.client.get('/api/summary/').data['burned'],150)
