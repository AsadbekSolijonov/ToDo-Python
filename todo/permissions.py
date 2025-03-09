# 1. AllowAny - Barchaga bir-xil hamma huquqlarni beradi.

# 2. IsAuthenticated - Login qilgan bo'lsa hamma huquqlarni beradi.

# 3. IsAdminUser - U Admin bo'lsa barcha huquqlarni beradi.

# 4. IsAthenticatedOrReadOnly - Login qilgan bo'lsa barcha huquqlar beriladi,
# aks holda xavsiz-o'qish uchun ko'rinadi.

from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Obyekt darajadagi ruxsat"""
        if request.user == obj.user or request.user.is_superuser:
            return True
        return False


class IsTaskOwnerOrSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Task obyekt darajadagi ruxsat"""
        if request.user == obj.category.user or request.user.is_superuser:
            return True
        return False
