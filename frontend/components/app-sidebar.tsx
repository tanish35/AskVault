"use client"

import { usePathname, useRouter } from "next/navigation"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
} from "@/components/ui/sidebar"
import { Button } from "@/components/ui/button"
import { HardDrive, MessageSquare, LogOut, FileText } from "lucide-react"
import axios from "@/lib/axios"

const menuItems = [
  {
    title: "Drive",
    url: "/dashboard/drive",
    icon: HardDrive,
  },
  {
    title: "Chat",
    url: "/dashboard/chat",
    icon: MessageSquare,
  },
]

export function AppSidebar() {
  const pathname = usePathname()
  const router = useRouter()

  const handleLogout = () => {
    axios
      .post("/api/user/logout", {}, { withCredentials: true })
      .then(() => {
        router.push("/login")
      })
      .catch((error) => {
        console.error("Logout failed:", error)
      })
  }

  return (
    <Sidebar>
      <SidebarHeader className="border-b">
        <div className="flex items-center space-x-2 px-2 py-2">
          <FileText className="h-6 w-6 text-blue-600" />
          <span className="font-semibold text-lg">AskVault</span>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {menuItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild isActive={pathname === item.url}>
                    <a href={item.url}>
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="border-t">
        <SidebarMenu>
          <SidebarMenuItem>
            <Button variant="ghost" className="w-full justify-start" onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
