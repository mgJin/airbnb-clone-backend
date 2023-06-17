from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):
    NAME = "am test"
    DESC = "am des"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "not 200",
        )

        self.assertIsInstance(
            data,
            list,
            "not list",
        )
        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):
        new_am_name = "new am"
        new_des_name = "new desc"

        response = self.client.post(
            self.URL,
            data={
                "name": new_am_name,
                "description": new_des_name,
            },
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "not 200",
        )

        self.assertEqual(
            data["name"],
            new_am_name,
            "not eq name",
        )

        self.assertEqual(
            data["description"],
            new_des_name,
            "not eq des",
        )

        response = self.client.post(self.URL)
        data = response.json()
        self.assertEqual(
            response.status_code,
            400,
            "not 400",
        )

        self.assertIn(
            "name",
            data,
            "not in",
        )


class TestAmenity(APITestCase):
    NAME = "test am"
    DESC = "test DESC"
    URL = "/api/v1/rooms/amenities/1"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2")

        self.assertEqual(
            response.status_code,
            404,
            "not 404",
        )

    def test_get_amenity(self):
        response = self.client.get(self.URL)

        self.assertEqual(
            response.status_code,
            200,
            "not 200",
        )

        data = response.json()

        self.assertEqual(
            data["name"],
            self.NAME,
            "not eq name",
        )

        self.assertEqual(
            data["description"],
            self.DESC,
            "not eq desc",
        )

    def test_put_amenity(self):
        put_name = "gimo"
        put_desc = "pretty"
        failure_name = "abcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcde"
        # 정상적
        response = self.client.put(
            self.URL,
            data={
                "name": put_name,
                "description": put_desc,
            },
        )

        self.assertEqual(response.status_code, 200, "not 200")
        data = response.json()
        self.assertEqual(
            data["name"],
            put_name,
            "not eq name",
        )
        self.assertEqual(
            data["description"],
            put_desc,
            "not eq desc",
        )
        # 빈 것 보냈을 때
        rseponse = self.client.put(self.URL)
        data_1 = rseponse.json()
        self.assertIn(
            "name",
            data,
            "not in",
        )
        # 글자수 제한 넘길 때
        response = self.client.put(
            self.URL,
            data={
                "name": failure_name,
                "description": put_desc,
            },
        )

        self.assertEqual(response.status_code, 400, "not 200 in fail")

        # 일부만 보냈을 때
        response = self.client.put(
            self.URL,
            data={
                "description": put_desc,
            },
        )

        data = response.json()
        self.assertEqual(response.status_code, 200, "not 200")
        self.assertEqual(
            data["description"],
            put_desc,
            "not eq desc",
        )

    def test_delete_amentiey(self):
        response = self.client.delete(self.URL)

        self.assertEqual(
            response.status_code,
            204,
            "not 204",
        )


class TestRooms(APITestCase):
    URL = "/api/v1/rooms/"

    def setUp(self):
        user = User.objects.create(
            username="test",
        )

        user.set_password("1234")
        user.save()

        self.user = user

    def test_create_room(self):
        response = self.client.post(self.URL)

        self.assertEqual(response.status_code, 403, "not 403")

        self.client.force_login(
            self.user,
        )
        response = self.client.post(self.URL)

        data = response.json()

        print(data)
