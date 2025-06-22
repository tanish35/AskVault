"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import axios from "@/lib/axios"

export default function HomePage() {
  const router = useRouter()

  useEffect(() => {
    const checkAuth = async () => {
      const isLoggedIn = await axios
        .get("/api/user/me", { withCredentials: true })
        .then((response) => response.status === 200)
        .catch(() => false)

      if (isLoggedIn) {
        router.push("/dashboard")
      } else {
        router.push("/login")
      }
    }

    checkAuth()
  }, [router])

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
    </div>
  )
}
