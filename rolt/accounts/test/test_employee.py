from unittest.mock import patch

import pytest
from model_bakery import baker
from rest_framework import status

from rolt.common.utils import make_mock_object


@pytest.mark.django_db
class TestEmployee:
    def test_if_employee_can_get_customer_list_return_200(
        self,
        make_employee_is_support_agent,
        api_client,
    ):
        make_employee_is_support_agent()
        response = api_client.get("/accounts/customers/")
        assert response.status_code == status.HTTP_200_OK

    def test_if_employee_can_get_filtered_customer_list_return_200(
        self,
        make_employee_is_support_agent,
        api_client,
    ):
        make_employee_is_support_agent()

        baker.make(
            "users.BaseUser",
            is_staff=False,
            first_name="Paul",
            last_name="Walker",
            email="paul@example.com",
        )

        response = api_client.get("/accounts/customers/?is_staff=False")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["user"]["first_name"] == "Paul"
        assert response.data["results"][0]["user"]["last_name"] == "Walker"

    def test_if_employee_can_get_customer_detail_return_200(
        self,
        make_employee_is_support_agent,
        api_client,
    ):
        make_employee_is_support_agent()

        # Create a mock user
        mock_user = make_mock_object(
            id="123e4567-e89b-12d3-a456-426614174003",
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
        )

        # Create a mock customer with user
        mock_customer = make_mock_object(
            id="123e4567-e89b-12d3-a456-426614174004",
            phone="0987654321",
            address="Old Address",
            birth_date="1990-01-01",
            user=mock_user,
        )

        # Mock CustomerSelector
        with patch(
            "rolt.accounts.selectors.customer_selector.CustomerSelector.customer_get",
            return_value=mock_customer,
        ):
            response = api_client.get(
                "/accounts/customers/123e4567-e89b-12d3-a456-426614174004/",
            )
            assert response.status_code == status.HTTP_200_OK
            assert response.data["phone"] == "0987654321"
            assert response.data["address"] == "Old Address"
            assert response.data["birth_date"] == "1990-01-01"
