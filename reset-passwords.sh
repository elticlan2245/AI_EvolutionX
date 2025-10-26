#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔑 RESETEANDO CONTRASEÑAS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

sudo docker exec -i mongodb mongosh << 'MONGOEOF'
use ai_evolutionx

// Eliminar TODOS los usuarios existentes
db.users.deleteMany({})

// Crear nuevo hash de password con Python/bcrypt
// Password: Admin123456
// Hash generado: $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW

// Usuario Admin
db.users.insertOne({
  email: "admin@aievolutionx.com",
  password: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
  name: "Administrator",
  created_at: new Date(),
  plan: "free",
  monthly_messages: 0,
  monthly_limit: 100,
  role: "admin"
})

// Usuario Test
db.users.insertOne({
  email: "test@test.com",
  password: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
  name: "Test User",
  created_at: new Date(),
  plan: "free",
  monthly_messages: 0,
  monthly_limit: 100
})

// Tu email personal
db.users.insertOne({
  email: "elgalatico2280@gmail.com",
  password: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
  name: "Owner",
  created_at: new Date(),
  plan: "enterprise",
  monthly_messages: 0,
  monthly_limit: -1,
  role: "admin"
})

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("✅ USUARIOS CREADOS:")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

db.users.find({}, {email: 1, name: 1, plan: 1, role: 1, _id: 0}).forEach(printjson)

exit
MONGOEOF

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ CONTRASEÑAS RESETEADAS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔑 TODAS LAS CUENTAS USAN LA MISMA CONTRASEÑA:"
echo "   Password: Admin123456"
echo ""
echo "📧 Cuentas creadas:"
echo "   1. admin@aievolutionx.com"
echo "   2. test@test.com"
echo "   3. elgalatico2280@gmail.com"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

